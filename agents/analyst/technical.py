from typing import Dict, List, Any
from datetime import datetime


class TechnicalAnalyzer:
    """Analyzes technical SEO data"""
    
    def __init__(self, config: Dict, prompts: Dict):
        self.config = config
        self.prompts = prompts
        self.thresholds = config.get('THRESHOLDS', {})
        
    def analyze(self, data: List[Dict], report: Dict) -> List[Dict[str, Any]]:
        """
        Analyze technical SEO data
        
        Returns list of insights with findings and recommendations
        """
        insights = []
        
        # 1. Identify error pages
        errors = self._find_error_pages(data)
        if errors:
            insights.append({
                "id": f"tech_errors_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "technical",
                "category": "crawl_errors",
                "severity": "high",
                "finding": f"Found {len(errors)} pages with errors",
                "affected_items": [item.get('url', 'N/A') for item in errors[:10]],
                "metrics": {
                    "4xx_errors": len([e for e in errors if e.get('status_code', 0) >= 400 and e.get('status_code', 0) < 500]),
                    "5xx_errors": len([e for e in errors if e.get('status_code', 0) >= 500]),
                    "total_errors": len(errors)
                },
                "recommendation": "Fix 404 errors with redirects or restore content. Resolve 5xx server errors immediately as they impact crawling."
            })
        
        # 2. Non-indexable pages
        non_indexable = self._find_non_indexable(data)
        if non_indexable:
            insights.append({
                "id": f"tech_indexability_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "technical",
                "category": "indexation_errors",
                "severity": "high",
                "finding": f"{len(non_indexable)} important pages are non-indexable",
                "affected_items": [item.get('url', 'N/A') for item in non_indexable[:10]],
                "metrics": {
                    "count": len(non_indexable)
                },
                "recommendation": "Review robots.txt, meta robots, and X-Robots-Tag headers. Ensure important content is indexable."
            })
        
        # 3. Core Web Vitals issues
        cwv_issues = self._find_core_web_vitals_issues(data)
        if cwv_issues:
            insights.append({
                "id": f"tech_cwv_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "technical",
                "category": "core_web_vitals",
                "severity": "high",
                "finding": f"{len(cwv_issues)} pages failing Core Web Vitals",
                "affected_items": [item.get('url', 'N/A') for item in cwv_issues[:10]],
                "metrics": {
                    "poor_lcp": len([p for p in cwv_issues if p.get('lcp', 0) > 2.5]),
                    "poor_fid": len([p for p in cwv_issues if p.get('fid', 0) > 100]),
                    "poor_cls": len([p for p in cwv_issues if p.get('cls', 0) > 0.1]),
                    "total": len(cwv_issues)
                },
                "recommendation": "Optimize images, reduce JavaScript, improve server response time. Focus on LCP, FID, and CLS improvements."
            })
        
        # 4. Slow pages
        slow_pages = self._find_slow_pages(data)
        if slow_pages:
            insights.append({
                "id": f"tech_speed_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "technical",
                "category": "page_speed",
                "severity": "medium",
                "finding": f"{len(slow_pages)} pages with slow load times",
                "affected_items": [item.get('url', 'N/A') for item in slow_pages[:10]],
                "metrics": {
                    "count": len(slow_pages),
                    "avg_load_time": self._avg_load_time(slow_pages)
                },
                "recommendation": "Implement caching, compress images, minify CSS/JS. Target load time under 3 seconds."
            })
        
        # 5. Deep crawl depth issues
        deep_pages = self._find_deep_pages(data)
        if deep_pages:
            insights.append({
                "id": f"tech_crawl_depth_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "module": "technical",
                "category": "crawl_depth",
                "severity": "medium",
                "finding": f"{len(deep_pages)} pages with deep crawl depth (>3 clicks)",
                "affected_items": [item.get('url', 'N/A') for item in deep_pages[:10]],
                "metrics": {
                    "count": len(deep_pages),
                    "avg_depth": self._avg_depth(deep_pages)
                },
                "recommendation": "Improve internal linking structure. Important pages should be within 3 clicks from homepage."
            })
        
        return insights
    
    def _find_error_pages(self, data: List[Dict]) -> List[Dict]:
        """Find pages with 4xx or 5xx status codes"""
        errors = []
        for item in data:
            status = item.get('status_code', 200)
            if status >= 400:
                errors.append(item)
        return errors
    
    def _find_non_indexable(self, data: List[Dict]) -> List[Dict]:
        """Find non-indexable pages with status 200"""
        non_indexable = []
        for item in data:
            status = item.get('status_code', 200)
            indexable = item.get('indexability', 'Yes')
            
            # Pages that are accessible but blocked from indexing
            if status == 200 and indexable in ['No', 'Blocked', False, 'false']:
                non_indexable.append(item)
        
        return non_indexable
    
    def _find_core_web_vitals_issues(self, data: List[Dict]) -> List[Dict]:
        """Find pages with poor Core Web Vitals"""
        issues = []
        
        for item in data:
            lcp = item.get('lcp', 0)
            fid = item.get('fid', 0)
            cls = item.get('cls', 0)
            
            # Google's thresholds: LCP < 2.5s, FID < 100ms, CLS < 0.1
            if lcp > 2.5 or fid > 100 or cls > 0.1:
                issues.append(item)
        
        return issues
    
    def _find_slow_pages(self, data: List[Dict]) -> List[Dict]:
        """Find pages with slow load times"""
        slow = []
        
        for item in data:
            load_time = item.get('load_time', 0)
            page_size = item.get('page_size', 0)
            
            # Pages loading slower than 3 seconds
            if load_time > 3:
                slow.append(item)
        
        return slow
    
    def _find_deep_pages(self, data: List[Dict]) -> List[Dict]:
        """Find pages with deep crawl depth"""
        deep = []
        
        for item in data:
            depth = item.get('crawl_depth', 0)
            
            # Pages more than 3 clicks from home
            if depth > 3:
                deep.append(item)
        
        return deep
    
    def _avg_load_time(self, items: List[Dict]) -> float:
        """Calculate average load time"""
        times = [item.get('load_time', 0) for item in items]
        return round(sum(times) / len(times), 2) if times else 0
    
    def _avg_depth(self, items: List[Dict]) -> float:
        """Calculate average crawl depth"""
        depths = [item.get('crawl_depth', 0) for item in items]
        return round(sum(depths) / len(depths), 1) if depths else 0
