"""
On-Page SEO Analysis Module
Analyzes metadata, content, schema, and on-page elements
"""

from typing import List, Dict, Any
from datetime import datetime


class OnPageAnalyzer:
    """Analyze on-page SEO elements"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.thresholds = config.get('THRESHOLDS', {})
    
    def analyze(self, data: List[Dict], parsed_report: Dict) -> List[Dict[str, Any]]:
        """
        Analyze on-page SEO data
        
        Expected data format:
        [
            {'url': '/page', 'title': 'Page Title', 'title_length': 55,
             'meta_description': 'Description', 'meta_length': 150,
             'h1_count': 1, 'h1_text': 'Heading', 'word_count': 500,
             'images': 10, 'images_no_alt': 3, 'internal_links': 15,
             'external_links': 5, 'schema_present': True}
        ]
        """
        insights = []
        
        if not data:
            return insights
        
        # Metadata analysis
        insights.extend(self._analyze_metadata(data))
        
        # Content analysis
        insights.extend(self._analyze_content(data))
        
        # Image optimization
        insights.extend(self._analyze_images(data))
        
        # Schema markup
        insights.extend(self._analyze_schema(data))
        
        # Internal linking
        insights.extend(self._analyze_internal_links(data))
        
        return insights
    
    def _analyze_metadata(self, data: List[Dict]) -> List[Dict]:
        """Analyze title tags and meta descriptions"""
        insights = []
        
        missing_titles = [p for p in data if not p.get('title') or len(p.get('title', '')) == 0]
        short_titles = [p for p in data if p.get('title_length', 0) < 30]
        long_titles = [p for p in data if p.get('title_length', 0) > 60]
        
        missing_meta = [p for p in data if not p.get('meta_description')]
        short_meta = [p for p in data if p.get('meta_length', 0) < 120]
        long_meta = [p for p in data if p.get('meta_length', 0) > 160]
        
        # Missing or problematic titles
        if missing_titles:
            insights.append({
                'id': f"onpage_titles_missing_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'metadata',
                'severity': 'high',
                'finding': f"{len(missing_titles)} pages missing title tags",
                'affected_items': [p.get('url', 'unknown') for p in missing_titles],
                'metrics': {'count': len(missing_titles)},
                'recommendation': "Add unique, descriptive title tags (50-60 characters) to all pages. Titles are critical for SEO and user experience."
            })
        
        if short_titles:
            insights.append({
                'id': f"onpage_titles_short_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'metadata',
                'severity': 'medium',
                'finding': f"{len(short_titles)} pages with short title tags (<30 chars)",
                'affected_items': [p.get('url', 'unknown') for p in short_titles[:10]],
                'metrics': {'count': len(short_titles)},
                'recommendation': "Expand title tags to be more descriptive. Optimal length is 50-60 characters for maximum visibility in search results."
            })
        
        if long_titles:
            insights.append({
                'id': f"onpage_titles_long_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'metadata',
                'severity': 'medium',
                'finding': f"{len(long_titles)} pages with long title tags (>60 chars)",
                'affected_items': [p.get('url', 'unknown') for p in long_titles[:10]],
                'metrics': {'count': len(long_titles)},
                'recommendation': "Shorten title tags to under 60 characters to prevent truncation in search results. Front-load important keywords."
            })
        
        # Meta descriptions
        if missing_meta:
            insights.append({
                'id': f"onpage_meta_missing_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'metadata',
                'severity': 'high',
                'finding': f"{len(missing_meta)} pages missing meta descriptions",
                'affected_items': [p.get('url', 'unknown') for p in missing_meta[:10]],
                'metrics': {'count': len(missing_meta)},
                'recommendation': "Write compelling meta descriptions (120-160 characters) for all pages. Include target keywords and clear CTAs to improve click-through rates."
            })
        
        return insights
    
    def _analyze_content(self, data: List[Dict]) -> List[Dict]:
        """Analyze content quality and structure"""
        insights = []
        
        thin_content = [p for p in data if p.get('word_count', 0) < 300]
        missing_h1 = [p for p in data if p.get('h1_count', 0) == 0]
        multiple_h1 = [p for p in data if p.get('h1_count', 0) > 1]
        
        if thin_content:
            insights.append({
                'id': f"onpage_thin_content_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'content',
                'severity': 'medium',
                'finding': f"{len(thin_content)} pages with thin content (<300 words)",
                'affected_items': [p.get('url', 'unknown') for p in thin_content[:10]],
                'metrics': {
                    'count': len(thin_content),
                    'avg_words': sum(p.get('word_count', 0) for p in thin_content) / len(thin_content) if thin_content else 0
                },
                'recommendation': "Expand content to at least 500-800 words. Add valuable information, FAQs, examples, and supporting details to increase relevance and engagement."
            })
        
        if missing_h1:
            insights.append({
                'id': f"onpage_missing_h1_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'content_structure',
                'severity': 'high',
                'finding': f"{len(missing_h1)} pages missing H1 heading tags",
                'affected_items': [p.get('url', 'unknown') for p in missing_h1[:10]],
                'metrics': {'count': len(missing_h1)},
                'recommendation': "Add a single, keyword-rich H1 tag to each page. H1 should clearly describe the page topic and match user intent."
            })
        
        if multiple_h1:
            insights.append({
                'id': f"onpage_multiple_h1_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'content_structure',
                'severity': 'low',
                'finding': f"{len(multiple_h1)} pages with multiple H1 tags",
                'affected_items': [p.get('url', 'unknown') for p in multiple_h1[:10]],
                'metrics': {'count': len(multiple_h1)},
                'recommendation': "Use only one H1 per page for proper content hierarchy. Use H2-H6 for subheadings."
            })
        
        return insights
    
    def _analyze_images(self, data: List[Dict]) -> List[Dict]:
        """Analyze image optimization"""
        insights = []
        
        pages_with_missing_alt = [p for p in data if p.get('images_no_alt', 0) > 0]
        
        if pages_with_missing_alt:
            total_missing = sum(p.get('images_no_alt', 0) for p in pages_with_missing_alt)
            insights.append({
                'id': f"onpage_missing_alt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'images',
                'severity': 'medium',
                'finding': f"{total_missing} images missing alt text across {len(pages_with_missing_alt)} pages",
                'affected_items': [p.get('url', 'unknown') for p in pages_with_missing_alt[:10]],
                'metrics': {
                    'total_images_no_alt': total_missing,
                    'pages_affected': len(pages_with_missing_alt)
                },
                'recommendation': "Add descriptive alt text to all images for accessibility and SEO. Include relevant keywords naturally while describing the image content."
            })
        
        return insights
    
    def _analyze_schema(self, data: List[Dict]) -> List[Dict]:
        """Analyze schema markup implementation"""
        insights = []
        
        pages_without_schema = [p for p in data if not p.get('schema_present', False)]
        
        if pages_without_schema and len(pages_without_schema) > len(data) * 0.5:
            insights.append({
                'id': f"onpage_schema_missing_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'structured_data',
                'severity': 'low',
                'finding': f"{len(pages_without_schema)} pages missing schema markup",
                'affected_items': [p.get('url', 'unknown') for p in pages_without_schema[:10]],
                'metrics': {'count': len(pages_without_schema)},
                'recommendation': "Implement structured data (Schema.org) for products, articles, FAQs, reviews, and local business. Helps search engines understand content and enables rich snippets."
            })
        
        return insights
    
    def _analyze_internal_links(self, data: List[Dict]) -> List[Dict]:
        """Analyze internal linking structure"""
        insights = []
        
        weak_internal_links = [p for p in data if p.get('internal_links', 0) < 3]
        
        if weak_internal_links:
            insights.append({
                'id': f"onpage_weak_internal_links_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'module': 'onpage',
                'category': 'internal_linking',
                'severity': 'medium',
                'finding': f"{len(weak_internal_links)} pages with weak internal linking (<3 links)",
                'affected_items': [p.get('url', 'unknown') for p in weak_internal_links[:10]],
                'metrics': {
                    'count': len(weak_internal_links),
                    'avg_links': sum(p.get('internal_links', 0) for p in weak_internal_links) / len(weak_internal_links) if weak_internal_links else 0
                },
                'recommendation': "Strengthen internal linking structure. Add contextual links to related content to improve navigation, distribute page authority, and help search engines discover content."
            })
        
        return insights
