"""
Historical Analyzer - Compare current vs historical data
Provides month-over-month, year-over-year, and trend analysis
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from statistics import mean, stdev
import math


class HistoricalAnalyzer:
    """Analyzes historical data to provide trends and comparisons"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    # ==================== COMPARISON ANALYSIS ====================
    
    def compare_month_over_month(self, client_id: int, metric_name: str) -> Dict:
        """Compare current month vs previous month"""
        metrics = self.db.get_metrics(client_id, metric_name)
        
        if len(metrics) < 2:
            return {"error": "Insufficient data for comparison"}
        
        current = metrics[0]
        previous = metrics[1]
        
        change = current['metric_value'] - previous['metric_value']
        change_percent = (change / previous['metric_value'] * 100) if previous['metric_value'] != 0 else 0
        
        return {
            'metric': metric_name,
            'current_value': current['metric_value'],
            'current_date': current['metric_date'],
            'previous_value': previous['metric_value'],
            'previous_date': previous['metric_date'],
            'change': change,
            'change_percent': round(change_percent, 2),
            'trend': 'up' if change > 0 else 'down' if change < 0 else 'flat'
        }
    
    def compare_year_over_year(self, client_id: int, metric_name: str) -> Dict:
        """Compare current vs same time last year"""
        today = date.today()
        year_ago = today - timedelta(days=365)
        
        current_metrics = self.db.get_metrics(
            client_id, metric_name, 
            start_date=today - timedelta(days=30)
        )
        
        year_ago_metrics = self.db.get_metrics(
            client_id, metric_name,
            start_date=year_ago - timedelta(days=30),
            end_date=year_ago
        )
        
        if not current_metrics or not year_ago_metrics:
            return {"error": "Insufficient historical data"}
        
        current_avg = mean(m['metric_value'] for m in current_metrics)
        year_ago_avg = mean(m['metric_value'] for m in year_ago_metrics)
        
        change = current_avg - year_ago_avg
        change_percent = (change / year_ago_avg * 100) if year_ago_avg != 0 else 0
        
        return {
            'metric': metric_name,
            'current_average': round(current_avg, 2),
            'year_ago_average': round(year_ago_avg, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'trend': 'up' if change > 0 else 'down' if change < 0 else 'flat'
        }
    
    def get_metric_summary(self, client_id: int, metric_name: str, months: int = 6) -> Dict:
        """Get comprehensive summary of a metric"""
        trend_data = self.db.get_metric_trend(client_id, metric_name, months)
        
        if not trend_data:
            return {"error": "No data available"}
        
        values = [d['metric_value'] for d in trend_data]
        
        return {
            'metric': metric_name,
            'period_months': months,
            'current_value': values[-1] if values else 0,
            'min_value': min(values),
            'max_value': max(values),
            'average_value': round(mean(values), 2),
            'std_deviation': round(stdev(values), 2) if len(values) > 1 else 0,
            'trend_direction': self._calculate_trend_direction(values),
            'volatility': self._calculate_volatility(values),
            'data_points': len(values),
            'timeline': trend_data
        }
    
    # ==================== KEYWORD ANALYSIS ====================
    
    def analyze_keyword_trends(self, client_id: int, keyword: str) -> Dict:
        """Analyze historical trends for a keyword"""
        history = self.db.get_keyword_history(client_id, keyword)
        
        if not history:
            return {"error": "No historical data for this keyword"}
        
        positions = [h['position'] for h in history if h['position']]
        clicks = [h['clicks'] for h in history if h['clicks']]
        
        return {
            'keyword': keyword,
            'first_tracked': history[0]['date'],
            'last_tracked': history[-1]['date'],
            'current_position': history[-1]['position'],
            'best_position': min(positions) if positions else None,
            'worst_position': max(positions) if positions else None,
            'average_position': round(mean(positions), 2) if positions else None,
            'position_improvement': history[0]['position'] - history[-1]['position'] if len(positions) > 1 else 0,
            'total_clicks': sum(clicks),
            'avg_monthly_clicks': round(mean(clicks), 2) if clicks else 0,
            'trend': self._calculate_trend_direction([p for p in positions if p]),
            'history': history
        }
    
    def compare_keyword_periods(self, client_id: int, days_back: int = 30) -> Dict:
        """Compare current vs previous period for all keywords"""
        cutoff_date = date.today() - timedelta(days=days_back)
        
        # Get current top keywords
        current_keywords = self.db.get_top_keywords(client_id, limit=100)
        
        comparisons = []
        for kw in current_keywords:
            history = self.db.get_keyword_history(client_id, kw['keyword'])
            
            if len(history) < 2:
                continue
            
            current = history[-1]
            # Find data from days_back ago
            previous = next(
                (h for h in reversed(history[:-1]) if h['date'] <= cutoff_date.isoformat()),
                history[0]
            )
            
            position_change = (previous['position'] or 0) - (current['position'] or 0)
            clicks_change = (current['clicks'] or 0) - (previous['clicks'] or 0)
            
            comparisons.append({
                'keyword': kw['keyword'],
                'current_position': current['position'],
                'previous_position': previous['position'],
                'position_change': round(position_change, 1),
                'current_clicks': current['clicks'],
                'previous_clicks': previous['clicks'],
                'clicks_change': clicks_change,
                'status': 'improved' if position_change > 0 else 'declined' if position_change < 0 else 'stable'
            })
        
        # Sort by impact (position improvement + clicks increase)
        comparisons.sort(
            key=lambda x: (x['position_change'] * 10 + x['clicks_change']), 
            reverse=True
        )
        
        winners = [c for c in comparisons if c['status'] == 'improved']
        losers = [c for c in comparisons if c['status'] == 'declined']
        
        return {
            'period_days': days_back,
            'total_keywords': len(comparisons),
            'improved': len(winners),
            'declined': len(losers),
            'stable': len([c for c in comparisons if c['status'] == 'stable']),
            'top_winners': winners[:10],
            'top_losers': losers[:10],
            'all_comparisons': comparisons
        }
    
    # ==================== PERFORMANCE ANALYSIS ====================
    
    def calculate_health_score_trend(self, client_id: int, months: int = 6) -> Dict:
        """Track health score over time"""
        reports = self.db.get_reports(client_id, limit=months)
        
        scores = [
            {'date': r['report_date'], 'score': r['health_score']}
            for r in reports if r['health_score']
        ]
        
        if not scores:
            return {"error": "No health score data available"}
        
        score_values = [s['score'] for s in scores]
        
        return {
            'current_score': scores[0]['score'],
            'average_score': round(mean(score_values), 2),
            'best_score': max(score_values),
            'worst_score': min(score_values),
            'improvement': scores[0]['score'] - scores[-1]['score'] if len(scores) > 1 else 0,
            'trend': self._calculate_trend_direction(score_values),
            'history': scores
        }
    
    def identify_top_improvements(self, client_id: int, limit: int = 10) -> List[Dict]:
        """Find metrics with biggest improvements"""
        # Get all unique metrics
        all_metrics = self.db.get_metrics(client_id)
        metric_names = set(m['metric_name'] for m in all_metrics)
        
        improvements = []
        for metric_name in metric_names:
            comparison = self.compare_month_over_month(client_id, metric_name)
            
            if 'error' not in comparison and comparison['change_percent'] != 0:
                improvements.append({
                    'metric': metric_name,
                    'change_percent': comparison['change_percent'],
                    'change_value': comparison['change'],
                    'current_value': comparison['current_value']
                })
        
        # Sort by absolute change percent
        improvements.sort(key=lambda x: abs(x['change_percent']), reverse=True)
        
        return improvements[:limit]
    
    def identify_concerning_trends(self, client_id: int) -> List[Dict]:
        """Find metrics with negative trends"""
        all_metrics = self.db.get_metrics(client_id)
        metric_names = set(m['metric_name'] for m in all_metrics)
        
        concerns = []
        for metric_name in metric_names:
            summary = self.get_metric_summary(client_id, metric_name, months=3)
            
            if 'error' in summary:
                continue
            
            # Flag if trending down with high volatility
            if summary['trend_direction'] == 'down':
                severity = 'high' if summary['volatility'] == 'high' else 'medium'
                concerns.append({
                    'metric': metric_name,
                    'trend': summary['trend_direction'],
                    'volatility': summary['volatility'],
                    'severity': severity,
                    'current_value': summary['current_value'],
                    'average': summary['average_value']
                })
        
        return sorted(concerns, key=lambda x: x['severity'], reverse=True)
    
    # ==================== HELPER METHODS ====================
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """Calculate overall trend direction using linear regression"""
        if len(values) < 2:
            return 'insufficient_data'
        
        n = len(values)
        x = list(range(n))
        
        # Simple linear regression
        x_mean = mean(x)
        y_mean = mean(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'flat'
        
        slope = numerator / denominator
        
        # Threshold for significance (adjust based on your needs)
        threshold = 0.01 * y_mean if y_mean != 0 else 0.01
        
        if slope > threshold:
            return 'up'
        elif slope < -threshold:
            return 'down'
        else:
            return 'flat'
    
    def _calculate_volatility(self, values: List[float]) -> str:
        """Calculate volatility level"""
        if len(values) < 2:
            return 'unknown'
        
        avg = mean(values)
        if avg == 0:
            return 'unknown'
        
        std = stdev(values)
        coefficient_of_variation = (std / avg) * 100
        
        if coefficient_of_variation < 10:
            return 'low'
        elif coefficient_of_variation < 25:
            return 'medium'
        else:
            return 'high'
    
    # ==================== REPORTING ====================
    
    def generate_trend_report(self, client_id: int) -> Dict:
        """Generate comprehensive trend analysis report"""
        client = self.db.get_client(client_id=client_id)
        
        if not client:
            return {"error": "Client not found"}
        
        # Get various analyses
        health_trend = self.calculate_health_score_trend(client_id)
        improvements = self.identify_top_improvements(client_id)
        concerns = self.identify_concerning_trends(client_id)
        keyword_comparison = self.compare_keyword_periods(client_id)
        
        return {
            'client_name': client['name'],
            'generated_at': datetime.now().isoformat(),
            'health_score_trend': health_trend,
            'top_improvements': improvements,
            'concerning_trends': concerns,
            'keyword_performance': {
                'improved': keyword_comparison.get('improved', 0),
                'declined': keyword_comparison.get('declined', 0),
                'top_winners': keyword_comparison.get('top_winners', []),
                'top_losers': keyword_comparison.get('top_losers', [])
            },
            'summary': {
                'total_metrics_tracked': len(improvements) + len(concerns),
                'positive_trends': len([i for i in improvements if i['change_percent'] > 0]),
                'negative_trends': len(concerns),
                'overall_health': 'improving' if len(improvements) > len(concerns) else 'declining'
            }
        }
