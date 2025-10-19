from typing import Dict, List, Any
from datetime import datetime


class KeywordsAnalyzer:
    """Analyzes keyword performance data"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.thresholds = config.get('THRESHOLDS', {})
        self.priorities = config.get('PRIORITIES', {})
        
    def analyze(self, data: List[Dict], report: Dict) -> List[Dict[str, Any]]:
        """
        Analyze keyword performance data
        
        Returns list of insights with findings and recommendations
        """
        insights = []
        
        # 1. Identify top performers
        top_keywords = self._find_top_performers(data)
        if top_keywords:
            insights.append({
                "id": f"kw_top_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "keywords",
                "category": "top_performers",
                "severity": "low",
                "finding": f"Identified {len(top_keywords)} top-performing keywords",
                "affected_items": [kw['query'] for kw in top_keywords],
                "metrics": {
                    "count": len(top_keywords),
                    "avg_position": self._avg_position(top_keywords),
                    "total_clicks": sum(kw.get('clicks', 0) for kw in top_keywords)
                },
                "recommendation": "Monitor these keywords closely and create supporting content to maintain rankings."
            })
        
        # 2. Identify declining keywords
        declining = self._find_declining_keywords(data)
        if declining:
            insights.append({
                "id": f"kw_decline_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "keywords",
                "category": "ranking_drop",
                "severity": "high",
                "finding": f"{len(declining)} keywords with significant position drops",
                "affected_items": [kw['query'] for kw in declining],
                "metrics": {
                    "count": len(declining),
                    "avg_drop": self._avg_drop(declining),
                    "estimated_traffic_loss": self._estimate_traffic_loss(declining)
                },
                "recommendation": "Review and update content for declining keywords. Check for competitor changes and content freshness."
            })
        
        # 3. Low CTR opportunities
        low_ctr = self._find_low_ctr_keywords(data)
        if low_ctr:
            insights.append({
                "id": f"kw_low_ctr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "keywords",
                "category": "low_ctr",
                "severity": "medium",
                "finding": f"{len(low_ctr)} keywords with good rankings but low CTR",
                "affected_items": [kw['query'] for kw in low_ctr[:10]],
                "metrics": {
                    "count": len(low_ctr),
                    "avg_ctr": self._avg_ctr(low_ctr),
                    "avg_position": self._avg_position(low_ctr)
                },
                "recommendation": "Optimize meta titles and descriptions to improve CTR. Add compelling copy and relevant keywords."
            })
        
        # 4. High impressions, low clicks
        high_imp_low_clicks = self._find_high_impressions_low_clicks(data)
        if high_imp_low_clicks:
            insights.append({
                "id": f"kw_opportunity_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "keywords",
                "category": "opportunity",
                "severity": "medium",
                "finding": f"{len(high_imp_low_clicks)} keywords with high visibility but underperforming clicks",
                "affected_items": [kw['query'] for kw in high_imp_low_clicks[:10]],
                "metrics": {
                    "count": len(high_imp_low_clicks),
                    "total_impressions": sum(kw.get('impressions', 0) for kw in high_imp_low_clicks),
                    "potential_clicks": self._estimate_click_potential(high_imp_low_clicks)
                },
                "recommendation": "Focus on improving rankings for these high-visibility terms to capture more traffic."
            })
        
        # 5. Keyword cannibalization (if URL data available)
        cannibalization = self._detect_cannibalization(data)
        if cannibalization:
            insights.append({
                "id": f"kw_cannibalization_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "keywords",
                "category": "cannibalization",
                "severity": "medium",
                "finding": f"Detected {len(cannibalization)} potential keyword cannibalization issues",
                "affected_items": list(cannibalization.keys())[:10],
                "metrics": {
                    "count": len(cannibalization)
                },
                "recommendation": "Consolidate content or clarify targeting for keywords with multiple competing URLs."
            })
        
        return insights
    
    def _find_top_performers(self, data: List[Dict]) -> List[Dict]:
        """Find top 10 keywords by clicks"""
        sorted_data = sorted(data, key=lambda x: x.get('clicks', 0), reverse=True)
        return sorted_data[:10]
    
    def _find_declining_keywords(self, data: List[Dict]) -> List[Dict]:
        """Find keywords with position drops"""
        declining = []
        
        for item in data:
            position = item.get('position')
            previous_position = item.get('previous_position')
            
            if position and previous_position:
                drop = position - previous_position
                if drop >= self.thresholds.get('ranking_drop_alert', 5):
                    item['position_drop'] = drop
                    declining.append(item)
        
        return declining
    
    def _find_low_ctr_keywords(self, data: List[Dict]) -> List[Dict]:
        """Find keywords with low CTR despite good rankings"""
        low_ctr = []
        ctr_threshold = self.thresholds.get('low_ctr_threshold', 2.0)
        
        for item in data:
            ctr = item.get('ctr', 0)
            position = item.get('position', 100)
            
            # Good rankings (top 10) but low CTR
            if position <= 10 and ctr < ctr_threshold:
                low_ctr.append(item)
        
        return low_ctr
    
    def _find_high_impressions_low_clicks(self, data: List[Dict]) -> List[Dict]:
        """Find keywords with high impressions but few clicks"""
        opportunities = []
        
        for item in data:
            impressions = item.get('impressions', 0)
            clicks = item.get('clicks', 0)
            
            if impressions > 100 and clicks < 10:
                opportunities.append(item)
        
        return sorted(opportunities, key=lambda x: x.get('impressions', 0), reverse=True)
    
    def _detect_cannibalization(self, data: List[Dict]) -> Dict[str, List[str]]:
        """Detect keywords with multiple ranking URLs"""
        keyword_urls = {}
        
        for item in data:
            query = item.get('query')
            url = item.get('url')
            
            if query and url:
                if query not in keyword_urls:
                    keyword_urls[query] = []
                if url not in keyword_urls[query]:
                    keyword_urls[query].append(url)
        
        # Return only keywords with multiple URLs
        return {k: v for k, v in keyword_urls.items() if len(v) > 1}
    
    def _avg_position(self, items: List[Dict]) -> float:
        """Calculate average position"""
        positions = [item.get('position', 0) for item in items if item.get('position')]
        return round(sum(positions) / len(positions), 2) if positions else 0
    
    def _avg_ctr(self, items: List[Dict]) -> float:
        """Calculate average CTR"""
        ctrs = [item.get('ctr', 0) for item in items if item.get('ctr')]
        return round(sum(ctrs) / len(ctrs), 2) if ctrs else 0
    
    def _avg_drop(self, items: List[Dict]) -> float:
        """Calculate average position drop"""
        drops = [item.get('position_drop', 0) for item in items]
        return round(sum(drops) / len(drops), 2) if drops else 0
    
    def _estimate_traffic_loss(self, items: List[Dict]) -> int:
        """Estimate traffic loss from position drops"""
        # Simple estimation: 5 positions ≈ 50% traffic loss
        total_clicks = sum(item.get('clicks', 0) for item in items)
        avg_drop = self._avg_drop(items)
        loss_percent = min(avg_drop * 10, 80) / 100
        return int(total_clicks * loss_percent)
    
    def _estimate_click_potential(self, items: List[Dict]) -> int:
        """Estimate potential clicks if CTR improves"""
        total_potential = 0
        for item in items:
            impressions = item.get('impressions', 0)
            # Assume 5% CTR potential for these opportunities
            total_potential += int(impressions * 0.05)
        return total_potential
