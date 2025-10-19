"""
Anomaly Detector - Identify unusual patterns in SEO data
Detects sudden drops, spikes, and abnormal behavior
"""

from datetime import date, timedelta
from typing import Dict, List, Tuple
from statistics import mean, stdev
import math


class AnomalyDetector:
    """Detect anomalies in SEO metrics"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        
        # Thresholds (configurable)
        self.z_score_threshold = 2.5  # Standard deviations
        self.percent_change_threshold = 30  # Percent
        
    # ==================== STATISTICAL ANOMALY DETECTION ====================
    
    def detect_metric_anomalies(self, client_id: int, metric_name: str, 
                               days: int = 90) -> List[Dict]:
        """Detect anomalies using statistical methods"""
        metrics = self.db.get_metrics(
            client_id, 
            metric_name,
            start_date=date.today() - timedelta(days=days)
        )
        
        if len(metrics) < 7:
            return []
        
        values = [m['metric_value'] for m in metrics]
        dates = [m['metric_date'] for m in metrics]
        
        # Calculate statistics
        avg = mean(values)
        std = stdev(values) if len(values) > 1 else 0
        
        if std == 0:
            return []
        
        # Find anomalies using Z-score method
        anomalies = []
        
        for i, value in enumerate(values):
            z_score = abs((value - avg) / std)
            
            if z_score > self.z_score_threshold:
                # Calculate expected value based on recent trend
                if i >= 7:
                    recent_avg = mean(values[i-7:i])
                else:
                    recent_avg = avg
                
                deviation = ((value - recent_avg) / recent_avg * 100) if recent_avg != 0 else 0
                
                severity = self._determine_severity(abs(deviation))
                
                anomalies.append({
                    'date': dates[i],
                    'metric': metric_name,
                    'actual_value': value,
                    'expected_value': round(recent_avg, 2),
                    'deviation_percent': round(deviation, 2),
                    'z_score': round(z_score, 2),
                    'type': 'spike' if value > recent_avg else 'drop',
                    'severity': severity
                })
                
                # Save to database
                self.db.save_anomaly(
                    client_id, metric_name, dates[i],
                    recent_avg, value, severity
                )
        
        return anomalies
    
    def detect_traffic_anomalies(self, client_id: int, days: int = 30) -> List[Dict]:
        """Detect traffic anomalies"""
        traffic = self.db.get_traffic_trend(client_id, days=days)
        
        if len(traffic) < 7:
            return []
        
        sessions = [t['total_sessions'] for t in traffic]
        dates = [t['date'] for t in traffic]
        
        # Use exponential moving average for comparison
        anomalies = []
        ema = sessions[0]
        alpha = 0.3
        
        for i in range(1, len(sessions)):
            ema = alpha * sessions[i-1] + (1 - alpha) * ema
            
            # Check if current value is significantly different
            percent_diff = ((sessions[i] - ema) / ema * 100) if ema != 0 else 0
            
            if abs(percent_diff) > self.percent_change_threshold:
                severity = self._determine_severity(abs(percent_diff))
                
                anomalies.append({
                    'date': dates[i],
                    'metric': 'traffic_sessions',
                    'actual_value': sessions[i],
                    'expected_value': round(ema, 0),
                    'deviation_percent': round(percent_diff, 2),
                    'type': 'spike' if percent_diff > 0 else 'drop',
                    'severity': severity
                })
                
                self.db.save_anomaly(
                    client_id, 'traffic_sessions', dates[i],
                    ema, sessions[i], severity
                )
        
        return anomalies
    
    # ==================== KEYWORD ANOMALY DETECTION ====================
    
    def detect_ranking_drops(self, client_id: int, position_threshold: int = 5) -> List[Dict]:
        """Detect sudden ranking drops"""
        keywords = self.db.get_top_keywords(client_id, limit=100)
        
        drops = []
        
        for kw in keywords:
            if kw['position_change'] and kw['position_change'] < -position_threshold:
                history = self.db.get_keyword_history(client_id, kw['keyword'])
                
                if len(history) >= 2:
                    current = history[-1]
                    previous = history[-2]
                    
                    # Estimate traffic impact
                    clicks_lost = previous['clicks'] - current['clicks']
                    
                    severity = 'critical' if abs(kw['position_change']) > 10 else 'high'
                    
                    drops.append({
                        'keyword': kw['keyword'],
                        'current_position': current['position'],
                        'previous_position': previous['position'],
                        'position_drop': abs(kw['position_change']),
                        'clicks_lost': clicks_lost,
                        'severity': severity,
                        'detected_at': date.today().isoformat()
                    })
        
        # Sort by impact
        drops.sort(key=lambda x: x['position_drop'], reverse=True)
        
        return drops
    
    def detect_keyword_cannibalization(self, client_id: int) -> List[Dict]:
        """Detect keyword cannibalization issues"""
        keywords = self.db.get_top_keywords(client_id, limit=200)
        
        # Group by keyword
        keyword_urls = {}
        for kw in keywords:
            if kw.get('url'):
                key = kw['keyword']
                if key not in keyword_urls:
                    keyword_urls[key] = []
                keyword_urls[key].append({
                    'url': kw['url'],
                    'position': kw['position'],
                    'clicks': kw['clicks']
                })
        
        # Find keywords ranking for multiple URLs
        cannibalization_issues = []
        
        for keyword, urls in keyword_urls.items():
            if len(urls) > 1:
                # Sort by position
                urls.sort(key=lambda x: x['position'])
                
                cannibalization_issues.append({
                    'keyword': keyword,
                    'competing_urls': len(urls),
                    'best_position': urls[0]['position'],
                    'worst_position': urls[-1]['position'],
                    'urls': urls,
                    'severity': 'high' if len(urls) > 2 else 'medium'
                })
        
        return cannibalization_issues
    
    # ==================== COMPREHENSIVE SCANS ====================
    
    def scan_all_anomalies(self, client_id: int) -> Dict:
        """Comprehensive anomaly scan"""
        client = self.db.get_client(client_id=client_id)
        
        if not client:
            return {"error": "Client not found"}
        
        # Run all detection methods
        metric_anomalies = []
        metrics = self.db.get_metrics(client_id)
        metric_names = set(m['metric_name'] for m in metrics)
        
        for metric_name in list(metric_names)[:10]:  # Limit to top 10 metrics
            anomalies = self.detect_metric_anomalies(client_id, metric_name)
            metric_anomalies.extend(anomalies)
        
        traffic_anomalies = self.detect_traffic_anomalies(client_id)
        ranking_drops = self.detect_ranking_drops(client_id)
        cannibalization = self.detect_keyword_cannibalization(client_id)
        
        # Get recent anomalies from database
        recent_anomalies = self.db.get_recent_anomalies(client_id, days=7)
        
        # Categorize by severity
        critical = []
        high = []
        medium = []
        
        for anomaly in metric_anomalies + traffic_anomalies:
            if anomaly['severity'] == 'critical':
                critical.append(anomaly)
            elif anomaly['severity'] == 'high':
                high.append(anomaly)
            else:
                medium.append(anomaly)
        
        for drop in ranking_drops:
            if drop['severity'] == 'critical':
                critical.append(drop)
            else:
                high.append(drop)
        
        return {
            'client_name': client['name'],
            'scan_date': date.today().isoformat(),
            'summary': {
                'total_anomalies': len(metric_anomalies) + len(traffic_anomalies),
                'ranking_drops': len(ranking_drops),
                'cannibalization_issues': len(cannibalization),
                'critical_count': len(critical),
                'high_count': len(high),
                'medium_count': len(medium)
            },
            'critical_issues': critical,
            'high_priority': high,
            'medium_priority': medium,
            'ranking_drops': ranking_drops[:10],
            'cannibalization': cannibalization[:5],
            'recent_anomalies': recent_anomalies,
            'recommendations': self._generate_anomaly_recommendations(
                critical, high, ranking_drops, cannibalization
            )
        }
    
    # ==================== ALERT GENERATION ====================
    
    def generate_alerts(self, client_id: int) -> List[Dict]:
        """Generate alerts for critical issues"""
        scan_results = self.scan_all_anomalies(client_id)
        
        alerts = []
        
        # Critical anomalies
        for issue in scan_results['critical_issues']:
            alerts.append({
                'type': 'critical_anomaly',
                'title': f"Critical {issue['type']} in {issue['metric']}",
                'message': f"Detected {issue['deviation_percent']}% deviation on {issue['date']}",
                'action': 'immediate_investigation_required',
                'priority': 1
            })
        
        # Ranking drops
        for drop in scan_results['ranking_drops'][:5]:
            alerts.append({
                'type': 'ranking_drop',
                'title': f"Ranking drop for '{drop['keyword']}'",
                'message': f"Dropped {drop['position_drop']} positions (now #{drop['current_position']})",
                'action': 'review_page_and_competitors',
                'priority': 2
            })
        
        # Cannibalization
        for issue in scan_results['cannibalization'][:3]:
            alerts.append({
                'type': 'cannibalization',
                'title': f"Keyword cannibalization: '{issue['keyword']}'",
                'message': f"{issue['competing_urls']} URLs competing for this keyword",
                'action': 'consolidate_or_differentiate_content',
                'priority': 3
            })
        
        return alerts
    
    # ==================== HELPER METHODS ====================
    
    def _determine_severity(self, deviation_percent: float) -> str:
        """Determine severity based on deviation"""
        if deviation_percent > 50:
            return 'critical'
        elif deviation_percent > 30:
            return 'high'
        elif deviation_percent > 15:
            return 'medium'
        else:
            return 'low'
    
    def _generate_anomaly_recommendations(self, critical: List, high: List, 
                                         ranking_drops: List, cannibalization: List) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if critical:
            recommendations.append("🔴 URGENT: Investigate critical anomalies immediately - check for technical issues, algorithm updates, or data collection problems")
        
        if ranking_drops:
            recommendations.append("📉 Review pages with ranking drops for content quality, technical issues, and competitor changes")
        
        if cannibalization:
            recommendations.append("🔀 Address keyword cannibalization by consolidating similar pages or differentiating content focus")
        
        if len(high) > 5:
            recommendations.append("⚠️ Multiple high-priority issues detected - prioritize investigation and allocate resources accordingly")
        
        if not (critical or high or ranking_drops):
            recommendations.append("✅ No critical issues detected - continue monitoring trends")
        
        return recommendations
