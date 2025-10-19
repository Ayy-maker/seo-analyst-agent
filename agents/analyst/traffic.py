"""
Traffic & Conversions Analysis Module
Analyzes traffic sources, user behavior, and conversion metrics
"""

from typing import List, Dict, Any
from datetime import datetime


class TrafficAnalyzer:
    """Analyze traffic and conversion metrics"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.thresholds = config.get('THRESHOLDS', {})
    
    def analyze(self, data: List[Dict], parsed_report: Dict) -> List[Dict[str, Any]]:
        """
        Analyze traffic data
        
        Expected data format:
        [
            {'page': '/page-url', 'sessions': 1000, 'users': 850,
             'pageviews': 1500, 'bounce_rate': 45.5, 'avg_session_duration': 120,
             'conversions': 25, 'conversion_rate': 2.5, 'source': 'organic',
             'device': 'mobile', 'country': 'US'}
        ]
        """
        insights = []
        
        if not data:
            return insights
        
        # Landing page performance
        insights.extend(self._analyze_landing_pages(data))
        
        # Traffic sources
        insights.extend(self._analyze_traffic_sources(data))
        
        # User engagement
        insights.extend(self._analyze_engagement(data))
        
        # Device performance
        insights.extend(self._analyze_devices(data))
        
        # Conversion analysis
        insights.extend(self._analyze_conversions(data))
        
        return insights
    
    def _analyze_landing_pages(self, data: List[Dict]) -> List[Dict]:
        """Analyze top and underperforming landing pages"""
        insights = []
        
        # Sort by sessions
        sorted_by_sessions = sorted(data, key=lambda x: x.get('sessions', 0), reverse=True)
        top_pages = sorted_by_sessions[:10]
        
        # High traffic pages
        if top_pages:
            total_sessions = sum(p.get('sessions', 0) for p in top_pages)
            insights.append({
                'id': f"traffic_top_pages_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'landing_pages',
                'severity': 'low',
                'finding': f"Top 10 landing pages driving {total_sessions} sessions",
                'affected_items': [p.get('page', 'unknown') for p in top_pages],
                'metrics': {
                    'total_sessions': total_sessions,
                    'avg_sessions': round(total_sessions / len(top_pages), 0),
                    'top_page_sessions': top_pages[0].get('sessions', 0) if top_pages else 0
                },
                'recommendation': "Focus optimization efforts on top-performing pages. Test different CTAs, improve content depth, add internal links to related products/services, and optimize for featured snippets."
            })
        
        # Pages with high bounce rate
        high_bounce = [p for p in data if p.get('bounce_rate', 0) > 70]
        if high_bounce:
            insights.append({
                'id': f"traffic_high_bounce_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'user_engagement',
                'severity': 'high',
                'finding': f"{len(high_bounce)} pages with high bounce rate (>70%)",
                'affected_items': [p.get('page', 'unknown') for p in high_bounce[:10]],
                'metrics': {
                    'count': len(high_bounce),
                    'avg_bounce_rate': round(sum(p.get('bounce_rate', 0) for p in high_bounce) / len(high_bounce), 1)
                },
                'recommendation': "Improve page content relevance, add engaging media (videos, images), create compelling CTAs, improve page load speed, and ensure content matches search intent. Target bounce rate under 50%."
            })
        
        # Low session duration pages
        low_duration = [p for p in data if p.get('avg_session_duration', 0) < 30]
        if low_duration:
            insights.append({
                'id': f"traffic_low_duration_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'user_engagement',
                'severity': 'medium',
                'finding': f"{len(low_duration)} pages with low average session duration (<30 seconds)",
                'affected_items': [p.get('page', 'unknown') for p in low_duration[:10]],
                'metrics': {
                    'count': len(low_duration),
                    'avg_duration': round(sum(p.get('avg_session_duration', 0) for p in low_duration) / len(low_duration), 1)
                },
                'recommendation': "Enhance content quality and depth. Add engaging elements like videos, infographics, and interactive content. Improve readability with better formatting, subheadings, and bullet points."
            })
        
        return insights
    
    def _analyze_traffic_sources(self, data: List[Dict]) -> List[Dict]:
        """Analyze traffic source distribution"""
        insights = []
        
        # Group by source
        sources = {}
        for page in data:
            source = page.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + page.get('sessions', 0)
        
        if sources:
            total_sessions = sum(sources.values())
            organic_sessions = sources.get('organic', 0)
            organic_percentage = (organic_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Organic traffic performance
            if organic_percentage > 40:
                insights.append({
                    'id': f"traffic_organic_strong_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'module': 'traffic',
                    'category': 'traffic_sources',
                    'severity': 'low',
                    'finding': f"Strong organic traffic: {round(organic_percentage, 1)}% of total sessions",
                    'affected_items': [f"Organic: {organic_sessions} sessions"],
                    'metrics': {
                        'organic_sessions': organic_sessions,
                        'organic_percentage': round(organic_percentage, 1),
                        'total_sessions': total_sessions
                    },
                    'recommendation': "Maintain SEO momentum with consistent content publishing, technical optimization, and link building. Monitor rankings closely and protect top-performing keywords."
                })
            elif organic_percentage < 20:
                insights.append({
                    'id': f"traffic_organic_weak_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'module': 'traffic',
                    'category': 'traffic_sources',
                    'severity': 'high',
                    'finding': f"Low organic traffic: only {round(organic_percentage, 1)}% of total sessions",
                    'affected_items': [f"Organic: {organic_sessions} sessions of {total_sessions} total"],
                    'metrics': {
                        'organic_sessions': organic_sessions,
                        'organic_percentage': round(organic_percentage, 1),
                        'total_sessions': total_sessions
                    },
                    'recommendation': "Urgent: Increase SEO efforts. Conduct comprehensive keyword research, optimize existing content, fix technical issues, build quality backlinks, and create content targeting high-intent keywords."
                })
        
        return insights
    
    def _analyze_engagement(self, data: List[Dict]) -> List[Dict]:
        """Analyze overall user engagement metrics"""
        insights = []
        
        if not data:
            return insights
        
        # Calculate averages
        total_pages = len(data)
        avg_bounce_rate = sum(p.get('bounce_rate', 0) for p in data) / total_pages
        avg_session_duration = sum(p.get('avg_session_duration', 0) for p in data) / total_pages
        avg_pageviews = sum(p.get('pageviews', 0) for p in data) / total_pages
        
        # Overall engagement assessment
        if avg_bounce_rate > 60:
            insights.append({
                'id': f"traffic_overall_engagement_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'engagement',
                'severity': 'medium',
                'finding': f"Site-wide average bounce rate is {round(avg_bounce_rate, 1)}% (above ideal 40-50%)",
                'affected_items': [f"Average across {total_pages} pages"],
                'metrics': {
                    'avg_bounce_rate': round(avg_bounce_rate, 1),
                    'avg_session_duration': round(avg_session_duration, 1),
                    'avg_pageviews': round(avg_pageviews, 1)
                },
                'recommendation': "Implement site-wide engagement improvements: better internal linking, prominent CTAs, related content suggestions, exit-intent popups, and improved page speed. Test different page layouts."
            })
        
        return insights
    
    def _analyze_devices(self, data: List[Dict]) -> List[Dict]:
        """Analyze device performance"""
        insights = []
        
        # Group by device
        devices = {}
        for page in data:
            device = page.get('device', 'unknown')
            if device not in devices:
                devices[device] = {'sessions': 0, 'bounce_rate': [], 'conversions': 0}
            
            devices[device]['sessions'] += page.get('sessions', 0)
            devices[device]['bounce_rate'].append(page.get('bounce_rate', 0))
            devices[device]['conversions'] += page.get('conversions', 0)
        
        # Calculate device metrics
        for device, metrics in devices.items():
            avg_bounce = sum(metrics['bounce_rate']) / len(metrics['bounce_rate']) if metrics['bounce_rate'] else 0
            metrics['avg_bounce_rate'] = avg_bounce
        
        # Mobile performance check
        if 'mobile' in devices:
            mobile_bounce = devices['mobile']['avg_bounce_rate']
            if mobile_bounce > 70:
                insights.append({
                    'id': f"traffic_mobile_experience_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'module': 'traffic',
                    'category': 'device_performance',
                    'severity': 'high',
                    'finding': f"Poor mobile experience: {round(mobile_bounce, 1)}% bounce rate on mobile devices",
                    'affected_items': [f"Mobile: {devices['mobile']['sessions']} sessions"],
                    'metrics': {
                        'mobile_bounce_rate': round(mobile_bounce, 1),
                        'mobile_sessions': devices['mobile']['sessions']
                    },
                    'recommendation': "Prioritize mobile optimization: improve page speed, simplify navigation, use larger touch targets, optimize forms for mobile, and ensure responsive design works perfectly across all screen sizes."
                })
        
        return insights
    
    def _analyze_conversions(self, data: List[Dict]) -> List[Dict]:
        """Analyze conversion performance"""
        insights = []
        
        pages_with_conversions = [p for p in data if p.get('conversions', 0) > 0]
        
        if pages_with_conversions:
            total_conversions = sum(p.get('conversions', 0) for p in pages_with_conversions)
            total_sessions = sum(p.get('sessions', 0) for p in data)
            overall_conv_rate = (total_conversions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Top converting pages
            top_converters = sorted(pages_with_conversions, 
                                   key=lambda x: x.get('conversion_rate', 0), 
                                   reverse=True)[:5]
            
            insights.append({
                'id': f"traffic_conversions_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'conversions',
                'severity': 'low',
                'finding': f"{len(pages_with_conversions)} pages generating conversions ({total_conversions} total)",
                'affected_items': [p.get('page', 'unknown') for p in top_converters],
                'metrics': {
                    'total_conversions': total_conversions,
                    'pages_converting': len(pages_with_conversions),
                    'overall_conv_rate': round(overall_conv_rate, 2),
                    'best_conv_rate': round(top_converters[0].get('conversion_rate', 0), 2) if top_converters else 0
                },
                'recommendation': "Analyze top converting pages for success patterns. Apply winning elements (CTAs, content structure, trust signals) to underperforming pages. Set up conversion funnel tracking to identify drop-off points."
            })
        else:
            insights.append({
                'id': f"traffic_no_conversions_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'traffic',
                'category': 'conversions',
                'severity': 'high',
                'finding': "No conversions tracked from organic traffic",
                'affected_items': ["All pages"],
                'metrics': {'total_conversions': 0},
                'recommendation': "Critical: Set up conversion tracking in Google Analytics 4. Define clear conversion goals (form submissions, purchases, phone calls). Create conversion-focused landing pages with strong CTAs."
            })
        
        return insights
