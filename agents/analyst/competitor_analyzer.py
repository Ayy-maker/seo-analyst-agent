"""
COMPETITOR ANALYSIS MODULE
Track and analyze competitor SEO performance
"""

from typing import Dict, List, Optional
from datetime import date, timedelta
from pathlib import Path


class CompetitorAnalyzer:
    """Analyze competitor SEO performance"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_competitor(self, client_id: int, competitor_domain: str, 
                      competitor_name: str = None) -> int:
        """Add a competitor to track"""
        
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO competitors (client_id, competitor_domain, competitor_name)
                   VALUES (?, ?, ?)
                   ON CONFLICT(client_id, competitor_domain) DO UPDATE SET
                   competitor_name = excluded.competitor_name""",
                (client_id, competitor_domain, competitor_name or competitor_domain)
            )
            return cursor.lastrowid
    
    def get_competitors(self, client_id: int) -> List[Dict]:
        """Get all competitors for a client"""
        
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """SELECT * FROM competitors WHERE client_id = ?""",
                (client_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def track_competitor_keyword(self, competitor_id: int, keyword: str, 
                                position: float, date_tracked: date = None):
        """Track a competitor's keyword position"""
        
        if date_tracked is None:
            date_tracked = date.today()
        
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO competitor_rankings 
                   (competitor_id, keyword, position, date)
                   VALUES (?, ?, ?, ?)""",
                (competitor_id, keyword, position, date_tracked)
            )
    
    def compare_keywords(self, client_id: int, competitor_id: int) -> Dict:
        """Compare keyword rankings between client and competitor"""
        
        # Get client keywords
        client_keywords = self.db.get_top_keywords(client_id, limit=100)
        
        # Get competitor keywords
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """SELECT keyword, AVG(position) as avg_position
                   FROM competitor_rankings
                   WHERE competitor_id = ?
                   AND date >= date('now', '-30 days')
                   GROUP BY keyword
                   ORDER BY avg_position ASC
                   LIMIT 100""",
                (competitor_id,)
            )
            competitor_keywords = [dict(row) for row in cursor.fetchall()]
        
        # Find gaps
        client_kw_set = set(kw['keyword'] for kw in client_keywords)
        competitor_kw_set = set(kw['keyword'] for kw in competitor_keywords)
        
        keyword_gaps = competitor_kw_set - client_kw_set
        shared_keywords = client_kw_set & competitor_kw_set
        
        # Compare shared keywords
        comparisons = []
        client_kw_dict = {kw['keyword']: kw for kw in client_keywords}
        competitor_kw_dict = {kw['keyword']: kw for kw in competitor_keywords}
        
        for keyword in shared_keywords:
            client_pos = client_kw_dict.get(keyword, {}).get('position', 100)
            competitor_pos = competitor_kw_dict.get(keyword, {}).get('avg_position', 100)
            
            comparisons.append({
                'keyword': keyword,
                'client_position': client_pos,
                'competitor_position': competitor_pos,
                'difference': client_pos - competitor_pos,
                'winning': client_pos < competitor_pos
            })
        
        # Sort by opportunity (where competitor ranks better)
        comparisons.sort(key=lambda x: -x['difference'])
        
        return {
            'total_client_keywords': len(client_keywords),
            'total_competitor_keywords': len(competitor_keywords),
            'keyword_gaps': list(keyword_gaps)[:20],
            'shared_keywords': len(shared_keywords),
            'winning': len([c for c in comparisons if c['winning']]),
            'losing': len([c for c in comparisons if not c['winning']]),
            'comparisons': comparisons[:20]
        }
    
    def get_competitor_insights(self, client_id: int) -> List[Dict]:
        """Generate insights from competitor analysis"""
        
        competitors = self.get_competitors(client_id)
        
        insights = []
        
        for competitor in competitors:
            comparison = self.compare_keywords(client_id, competitor['id'])
            
            # Keyword gap opportunities
            if comparison['keyword_gaps']:
                insights.append({
                    'module': 'competitor',
                    'type': 'opportunity',
                    'severity': 'medium',
                    'insight': f"Found {len(comparison['keyword_gaps'])} keyword opportunities where {competitor['competitor_name']} ranks but you don't: {', '.join(list(comparison['keyword_gaps'])[:3])}...",
                    'metric_value': len(comparison['keyword_gaps'])
                })
            
            # Performance comparison
            win_rate = (comparison['winning'] / comparison['shared_keywords'] * 100) if comparison['shared_keywords'] > 0 else 0
            
            if win_rate < 50:
                insights.append({
                    'module': 'competitor',
                    'type': 'issue',
                    'severity': 'high',
                    'insight': f"Losing to {competitor['competitor_name']} on {comparison['losing']} shared keywords ({100-win_rate:.1f}% of overlap). Focus on improving these rankings.",
                    'metric_value': comparison['losing']
                })
            elif win_rate > 70:
                insights.append({
                    'module': 'competitor',
                    'type': 'win',
                    'severity': 'low',
                    'insight': f"Outranking {competitor['competitor_name']} on {comparison['winning']} keywords ({win_rate:.1f}% win rate). Strong competitive position.",
                    'metric_value': comparison['winning']
                })
        
        return insights
    
    def analyze_competitor_backlinks(self, client_id: int, competitor_id: int) -> Dict:
        """Analyze competitor backlink profile (placeholder for future API integration)"""
        
        # This would integrate with APIs like Ahrefs, SEMrush, Moz
        # For now, return structure
        
        return {
            'status': 'pending',
            'message': 'Backlink analysis requires API integration',
            'future_features': [
                'Total backlinks comparison',
                'Referring domains analysis',
                'Link quality metrics',
                'Common link sources',
                'Link gap opportunities'
            ]
        }
    
    def generate_competitive_report(self, client_id: int) -> Dict:
        """Generate comprehensive competitive analysis report"""
        
        competitors = self.get_competitors(client_id)
        
        if not competitors:
            return {
                'status': 'no_competitors',
                'message': 'No competitors added yet. Add competitors to enable analysis.'
            }
        
        report = {
            'client_id': client_id,
            'competitors_tracked': len(competitors),
            'analysis_date': date.today().isoformat(),
            'competitors': []
        }
        
        for competitor in competitors:
            comp_analysis = self.compare_keywords(client_id, competitor['id'])
            
            report['competitors'].append({
                'name': competitor['competitor_name'],
                'domain': competitor['competitor_domain'],
                'keyword_comparison': comp_analysis,
                'added_date': competitor['added_at']
            })
        
        # Generate overall insights
        report['insights'] = self.get_competitor_insights(client_id)
        
        # Summary
        total_gaps = sum(len(c['keyword_comparison']['keyword_gaps']) for c in report['competitors'])
        total_shared = sum(c['keyword_comparison']['shared_keywords'] for c in report['competitors'])
        
        report['summary'] = {
            'total_keyword_gaps': total_gaps,
            'total_shared_keywords': total_shared,
            'top_opportunities': total_gaps,
            'competitive_strength': 'Strong' if total_gaps < 50 else 'Moderate' if total_gaps < 100 else 'Needs Work'
        }
        
        return report
