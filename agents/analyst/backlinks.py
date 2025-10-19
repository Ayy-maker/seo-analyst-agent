"""
Backlinks Analysis Module
Analyzes backlink profile, quality, and growth
"""

from typing import List, Dict, Any
from datetime import datetime


class BacklinksAnalyzer:
    """Analyze backlink profile and quality"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.thresholds = config.get('THRESHOLDS', {})
    
    def analyze(self, data: List[Dict], parsed_report: Dict) -> List[Dict[str, Any]]:
        """
        Analyze backlinks data
        
        Expected data format:
        [
            {'source_url': 'https://example.com/page', 'target_url': '/my-page',
             'anchor_text': 'keyword', 'domain_authority': 45, 'spam_score': 5,
             'link_type': 'dofollow', 'first_seen': '2024-01-01', 'status': 'active'}
        ]
        """
        insights = []
        
        if not data:
            return insights
        
        # Backlink quality analysis
        insights.extend(self._analyze_link_quality(data))
        
        # Anchor text analysis
        insights.extend(self._analyze_anchor_text(data))
        
        # Link growth/loss
        insights.extend(self._analyze_link_growth(data))
        
        # Toxic links
        insights.extend(self._analyze_toxic_links(data))
        
        # Domain diversity
        insights.extend(self._analyze_domain_diversity(data))
        
        return insights
    
    def _analyze_link_quality(self, data: List[Dict]) -> List[Dict]:
        """Analyze overall backlink quality"""
        insights = []
        
        if not data:
            return insights
        
        total_links = len(data)
        dofollow_links = [l for l in data if l.get('link_type', '').lower() == 'dofollow']
        high_authority = [l for l in data if l.get('domain_authority', 0) >= 50]
        low_authority = [l for l in data if l.get('domain_authority', 0) < 20]
        
        # High quality backlink achievement
        if high_authority:
            insights.append({
                'id': f"backlinks_high_authority_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'link_quality',
                'severity': 'low',
                'finding': f"Acquired {len(high_authority)} high-authority backlinks (DA 50+)",
                'affected_items': [l.get('source_url', 'unknown')[:100] for l in high_authority[:10]],
                'metrics': {
                    'count': len(high_authority),
                    'percentage': round((len(high_authority) / total_links) * 100, 1),
                    'avg_da': round(sum(l.get('domain_authority', 0) for l in high_authority) / len(high_authority), 1)
                },
                'recommendation': "Excellent work! Continue building relationships with high-authority domains. Monitor these links for status changes and explore opportunities for additional placements on these domains."
            })
        
        # Low authority warning
        if len(low_authority) > total_links * 0.4:
            insights.append({
                'id': f"backlinks_low_authority_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'link_quality',
                'severity': 'medium',
                'finding': f"{len(low_authority)} low-authority backlinks (DA <20) - {round((len(low_authority)/total_links)*100,1)}% of profile",
                'affected_items': [l.get('source_url', 'unknown')[:100] for l in low_authority[:10]],
                'metrics': {
                    'count': len(low_authority),
                    'percentage': round((len(low_authority) / total_links) * 100, 1)
                },
                'recommendation': "Focus link building efforts on higher-authority domains (DA 30+). Audit low-authority links for spam and consider disavowing harmful ones. Prioritize quality over quantity."
            })
        
        # Dofollow ratio
        dofollow_ratio = (len(dofollow_links) / total_links) * 100 if total_links > 0 else 0
        if dofollow_ratio < 60:
            insights.append({
                'id': f"backlinks_nofollow_ratio_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'link_attributes',
                'severity': 'medium',
                'finding': f"Only {round(dofollow_ratio, 1)}% of backlinks are dofollow",
                'affected_items': [f"{len(dofollow_links)} dofollow, {total_links - len(dofollow_links)} nofollow"],
                'metrics': {
                    'dofollow_count': len(dofollow_links),
                    'nofollow_count': total_links - len(dofollow_links),
                    'dofollow_ratio': round(dofollow_ratio, 1)
                },
                'recommendation': "Increase proportion of dofollow links through guest posting, PR campaigns, and partnerships with authoritative sites. Target 70-80% dofollow for optimal SEO value."
            })
        
        return insights
    
    def _analyze_anchor_text(self, data: List[Dict]) -> List[Dict]:
        """Analyze anchor text distribution"""
        insights = []
        
        if not data:
            return insights
        
        # Count anchor texts
        anchor_counts = {}
        for link in data:
            anchor = link.get('anchor_text', '').lower().strip()
            if anchor:
                anchor_counts[anchor] = anchor_counts.get(anchor, 0) + 1
        
        # Check for over-optimization
        if anchor_counts:
            max_anchor = max(anchor_counts.items(), key=lambda x: x[1])
            max_percentage = (max_anchor[1] / len(data)) * 100
            
            if max_percentage > 40:
                insights.append({
                    'id': f"backlinks_anchor_over_optimization_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'module': 'backlinks',
                    'category': 'anchor_text',
                    'severity': 'high',
                    'finding': f"Anchor text '{max_anchor[0]}' used in {round(max_percentage, 1)}% of backlinks",
                    'affected_items': [f"{max_anchor[0]}: {max_anchor[1]} occurrences"],
                    'metrics': {
                        'top_anchor': max_anchor[0],
                        'count': max_anchor[1],
                        'percentage': round(max_percentage, 1)
                    },
                    'recommendation': "Diversify anchor text to avoid over-optimization penalties. Use branded anchors, naked URLs, and varied natural phrases. Aim for 30-40% branded, 20-30% exact match, 30-50% natural variation."
                })
        
        return insights
    
    def _analyze_link_growth(self, data: List[Dict]) -> List[Dict]:
        """Analyze link acquisition and loss trends"""
        insights = []
        
        active_links = [l for l in data if l.get('status', '').lower() == 'active']
        lost_links = [l for l in data if l.get('status', '').lower() in ['lost', 'broken', '404']]
        
        if lost_links and len(lost_links) > len(data) * 0.1:
            insights.append({
                'id': f"backlinks_lost_links_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'link_status',
                'severity': 'high',
                'finding': f"{len(lost_links)} backlinks recently lost or broken",
                'affected_items': [l.get('source_url', 'unknown')[:100] for l in lost_links[:10]],
                'metrics': {
                    'lost_count': len(lost_links),
                    'percentage': round((len(lost_links) / len(data)) * 100, 1)
                },
                'recommendation': "Investigate lost backlinks and reach out to webmasters to restore them. Set up 301 redirects for broken target URLs. Monitor backlink health monthly to minimize losses."
            })
        
        return insights
    
    def _analyze_toxic_links(self, data: List[Dict]) -> List[Dict]:
        """Analyze potentially toxic or spammy backlinks"""
        insights = []
        
        toxic_threshold = self.thresholds.get('toxic_backlink_score', 30)
        toxic_links = [l for l in data if l.get('spam_score', 0) > toxic_threshold]
        
        if toxic_links:
            insights.append({
                'id': f"backlinks_toxic_links_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'toxic_links',
                'severity': 'high',
                'finding': f"{len(toxic_links)} potentially toxic backlinks detected (spam score >{toxic_threshold})",
                'affected_items': [l.get('source_url', 'unknown')[:100] for l in toxic_links[:10]],
                'metrics': {
                    'toxic_count': len(toxic_links),
                    'avg_spam_score': round(sum(l.get('spam_score', 0) for l in toxic_links) / len(toxic_links), 1),
                    'percentage': round((len(toxic_links) / len(data)) * 100, 1)
                },
                'recommendation': "Review toxic backlinks immediately. Create a disavow file for harmful links and submit to Google Search Console. Monitor regularly for new toxic links and take proactive action."
            })
        
        return insights
    
    def _analyze_domain_diversity(self, data: List[Dict]) -> List[Dict]:
        """Analyze referring domain diversity"""
        insights = []
        
        if not data:
            return insights
        
        # Extract domains
        referring_domains = set()
        for link in data:
            source = link.get('source_url', '')
            if source:
                # Extract domain from URL
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(source).netloc
                    referring_domains.add(domain)
                except:
                    pass
        
        domain_count = len(referring_domains)
        total_links = len(data)
        diversity_ratio = domain_count / total_links if total_links > 0 else 0
        
        if diversity_ratio < 0.3:  # Less than 30% unique domains
            insights.append({
                'id': f"backlinks_low_diversity_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'backlinks',
                'category': 'domain_diversity',
                'severity': 'medium',
                'finding': f"Low domain diversity: {domain_count} unique domains for {total_links} backlinks",
                'affected_items': list(referring_domains)[:10],
                'metrics': {
                    'unique_domains': domain_count,
                    'total_links': total_links,
                    'diversity_ratio': round(diversity_ratio * 100, 1)
                },
                'recommendation': "Improve referring domain diversity. Expand outreach to new websites, participate in industry forums, create link-worthy content, and pursue partnerships with varied authoritative domains."
            })
        
        return insights
