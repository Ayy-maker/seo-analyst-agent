"""
Competitive Benchmarking System
Compare SEO performance against industry standards and identify gaps
"""

from typing import Dict, List, Any, Optional


class CompetitiveBenchmarks:
    """
    Compare client performance against industry benchmarks
    Identify competitive strengths and weaknesses
    """

    # Industry-specific benchmarks based on industry data
    INDUSTRY_BENCHMARKS = {
        'automotive': {
            'avg_position': 15.2,
            'avg_ctr': {
                'overall': 4.5,
                'position_1-3': 28.0,
                'position_4-10': 12.0,
                'position_11-20': 5.0,
                'position_21+': 2.0
            },
            'mobile_percentage': 68,
            'local_search_percentage': 72,
            'branded_vs_nonbranded': 0.4,  # 40% branded searches
            'typical_impressions': 8500,
            'typical_clicks': 320,
            'conversion_rate': 15.0,  # 15% of clicks become leads
            'avg_transaction': 450,
            'seasonality': 'High (winter tyres Nov-Feb, summer Mar-May)'
        },
        'legal': {
            'avg_position': 12.8,
            'avg_ctr': {
                'overall': 3.8,
                'position_1-3': 32.0,
                'position_4-10': 15.0,
                'position_11-20': 6.0,
                'position_21+': 2.5
            },
            'mobile_percentage': 35,
            'local_search_percentage': 85,
            'branded_vs_nonbranded': 0.6,
            'typical_impressions': 6200,
            'typical_clicks': 245,
            'conversion_rate': 5.0,
            'avg_transaction': 15000,
            'seasonality': 'Low (relatively consistent year-round)'
        },
        'healthcare': {
            'avg_position': 14.5,
            'avg_ctr': {
                'overall': 4.2,
                'position_1-3': 30.0,
                'position_4-10': 13.0,
                'position_11-20': 5.5,
                'position_21+': 2.2
            },
            'mobile_percentage': 62,
            'local_search_percentage': 78,
            'branded_vs_nonbranded': 0.5,
            'typical_impressions': 7200,
            'typical_clicks': 290,
            'conversion_rate': 8.0,
            'avg_transaction': 850,
            'seasonality': 'Medium (Q1 surge for new insurance/resolutions)'
        },
        'real_estate': {
            'avg_position': 18.3,
            'avg_ctr': {
                'overall': 3.5,
                'position_1-3': 25.0,
                'position_4-10': 10.0,
                'position_11-20': 4.5,
                'position_21+': 1.8
            },
            'mobile_percentage': 42,
            'local_search_percentage': 92,
            'branded_vs_nonbranded': 0.7,
            'typical_impressions': 9800,
            'typical_clicks': 350,
            'conversion_rate': 3.0,
            'avg_transaction': 22000,
            'seasonality': 'High (Spring/Fall peaks, Winter slow)'
        },
        'restaurant': {
            'avg_position': 10.2,
            'avg_ctr': {
                'overall': 5.0,
                'position_1-3': 35.0,
                'position_4-10': 16.0,
                'position_11-20': 6.5,
                'position_21+': 2.5
            },
            'mobile_percentage': 75,
            'local_search_percentage': 88,
            'branded_vs_nonbranded': 0.3,
            'typical_impressions': 11500,
            'typical_clicks': 520,
            'conversion_rate': 12.0,
            'avg_transaction': 95,
            'seasonality': 'Medium (weekends, holidays, events)'
        },
        'general': {
            'avg_position': 16.0,
            'avg_ctr': {
                'overall': 4.0,
                'position_1-3': 28.0,
                'position_4-10': 12.0,
                'position_11-20': 5.0,
                'position_21+': 2.0
            },
            'mobile_percentage': 55,
            'local_search_percentage': 50,
            'branded_vs_nonbranded': 0.5,
            'typical_impressions': 7500,
            'typical_clicks': 300,
            'conversion_rate': 5.0,
            'avg_transaction': 500,
            'seasonality': 'Variable'
        }
    }

    def compare_performance(self, data: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """
        Compare client performance against industry benchmarks

        Args:
            data: Client performance data
            industry: Industry identifier

        Returns:
            Comprehensive benchmark comparison
        """
        benchmarks = self.INDUSTRY_BENCHMARKS.get(industry, self.INDUSTRY_BENCHMARKS['general'])

        comparison = {
            'industry': industry,
            'benchmarks': benchmarks,
            'performance': {},
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'overall_score': 0
        }

        # Compare position
        client_position = data.get('avg_position', data.get('position_avg', 20))
        position_performance = self._compare_position(client_position, benchmarks['avg_position'])
        comparison['performance']['position'] = position_performance

        # Compare CTR
        client_ctr = data.get('avg_ctr', data.get('ctr', 0))
        ctr_performance = self._compare_ctr(client_ctr, benchmarks['avg_ctr']['overall'])
        comparison['performance']['ctr'] = ctr_performance

        # Compare mobile usage
        client_mobile = self._get_mobile_percentage(data)
        mobile_performance = self._compare_percentage(
            client_mobile,
            benchmarks['mobile_percentage'],
            'Mobile Traffic'
        )
        comparison['performance']['mobile'] = mobile_performance

        # Compare clicks/impressions
        client_clicks = data.get('clicks', data.get('total_clicks', 0))
        client_impressions = data.get('impressions', data.get('total_impressions', 0))

        clicks_performance = self._compare_absolute(
            client_clicks,
            benchmarks['typical_clicks'],
            'Total Clicks'
        )
        impressions_performance = self._compare_absolute(
            client_impressions,
            benchmarks['typical_impressions'],
            'Total Impressions'
        )

        comparison['performance']['clicks'] = clicks_performance
        comparison['performance']['impressions'] = impressions_performance

        # Identify strengths and weaknesses
        comparison['strengths'], comparison['weaknesses'] = self._categorize_performance(comparison['performance'])

        # Calculate overall performance score (0-100)
        comparison['overall_score'] = self._calculate_overall_score(comparison['performance'])

        # Identify opportunities
        comparison['opportunities'] = self._identify_opportunities(comparison['weaknesses'], benchmarks)

        return comparison

    def _compare_position(self, client: float, benchmark: float) -> Dict[str, Any]:
        """Compare average position (lower is better)"""
        difference = benchmark - client  # Positive = better than benchmark
        percentage = (difference / benchmark) * 100

        return {
            'client_value': round(client, 1),
            'benchmark_value': round(benchmark, 1),
            'difference': round(difference, 1),
            'percentage': round(percentage, 1),
            'rating': self._get_position_rating(percentage),
            'status': 'outperforming' if difference > 0 else 'underperforming'
        }

    def _compare_ctr(self, client: float, benchmark: float) -> Dict[str, Any]:
        """Compare CTR (higher is better)"""
        difference = client - benchmark
        percentage = (difference / benchmark) * 100 if benchmark > 0 else 0

        return {
            'client_value': round(client, 2),
            'benchmark_value': round(benchmark, 2),
            'difference': round(difference, 2),
            'percentage': round(percentage, 1),
            'rating': self._get_ctr_rating(percentage),
            'status': 'outperforming' if difference > 0 else 'underperforming'
        }

    def _compare_percentage(self, client: float, benchmark: float, metric_name: str) -> Dict[str, Any]:
        """Compare percentage metrics"""
        difference = client - benchmark
        percentage_diff = difference  # Already in percentage points

        return {
            'metric_name': metric_name,
            'client_value': round(client, 1),
            'benchmark_value': round(benchmark, 1),
            'difference': round(difference, 1),
            'rating': self._get_percentage_rating(abs(difference)),
            'status': 'on par' if abs(difference) < 5 else ('above' if difference > 0 else 'below')
        }

    def _compare_absolute(self, client: int, benchmark: int, metric_name: str) -> Dict[str, Any]:
        """Compare absolute numbers (clicks, impressions)"""
        difference = client - benchmark
        percentage = (difference / benchmark) * 100 if benchmark > 0 else 0

        return {
            'metric_name': metric_name,
            'client_value': client,
            'benchmark_value': benchmark,
            'difference': difference,
            'percentage': round(percentage, 1),
            'rating': self._get_absolute_rating(percentage),
            'status': 'outperforming' if difference > 0 else 'underperforming'
        }

    def _get_position_rating(self, percentage: float) -> str:
        """Rate position performance (positive = better)"""
        if percentage > 30:
            return 'Excellent'
        elif percentage > 15:
            return 'Good'
        elif percentage > 0:
            return 'Average'
        elif percentage > -15:
            return 'Below Average'
        else:
            return 'Poor'

    def _get_ctr_rating(self, percentage: float) -> str:
        """Rate CTR performance"""
        if percentage > 25:
            return 'Excellent'
        elif percentage > 10:
            return 'Good'
        elif percentage > -5:
            return 'Average'
        elif percentage > -20:
            return 'Below Average'
        else:
            return 'Poor'

    def _get_percentage_rating(self, difference: float) -> str:
        """Rate percentage-based metrics"""
        if difference < 5:
            return 'On Target'
        elif difference < 15:
            return 'Slight Variance'
        else:
            return 'Significant Variance'

    def _get_absolute_rating(self, percentage: float) -> str:
        """Rate absolute metrics performance"""
        if percentage > 50:
            return 'Excellent'
        elif percentage > 20:
            return 'Good'
        elif percentage > -10:
            return 'Average'
        elif percentage > -30:
            return 'Below Average'
        else:
            return 'Poor'

    def _get_mobile_percentage(self, data: Dict[str, Any]) -> float:
        """Extract mobile percentage from data"""
        if 'devices' in data:
            devices = data['devices']
            if isinstance(devices, dict):
                return devices.get('mobile', 50.0)
            elif isinstance(devices, list):
                mobile_device = next((d for d in devices if d.get('device') == 'Mobile'), None)
                if mobile_device:
                    return mobile_device.get('percentage', 50.0)
        return 50.0  # Default

    def _categorize_performance(self, performance: Dict[str, Any]) -> tuple:
        """Categorize metrics into strengths and weaknesses"""
        strengths = []
        weaknesses = []

        for metric, data in performance.items():
            rating = data.get('rating', 'Average')
            status = data.get('status', 'on par')

            if rating in ['Excellent', 'Good'] or status == 'outperforming':
                strengths.append({
                    'metric': metric,
                    'rating': rating,
                    'description': f"{data.get('metric_name', metric)}: {rating}"
                })
            elif rating in ['Below Average', 'Poor'] or status == 'underperforming':
                weaknesses.append({
                    'metric': metric,
                    'rating': rating,
                    'description': f"{data.get('metric_name', metric)}: {rating}"
                })

        return strengths, weaknesses

    def _calculate_overall_score(self, performance: Dict[str, Any]) -> int:
        """Calculate overall performance score (0-100)"""
        rating_scores = {
            'Excellent': 100,
            'Good': 80,
            'Average': 60,
            'On Target': 70,
            'Slight Variance': 50,
            'Below Average': 40,
            'Poor': 20,
            'Significant Variance': 30
        }

        scores = []
        for metric_data in performance.values():
            rating = metric_data.get('rating', 'Average')
            scores.append(rating_scores.get(rating, 60))

        return round(sum(scores) / len(scores)) if scores else 60

    def _identify_opportunities(self, weaknesses: List[Dict], benchmarks: Dict) -> List[Dict]:
        """Identify improvement opportunities from weaknesses"""
        opportunities = []

        for weakness in weaknesses:
            metric = weakness['metric']

            if metric == 'position':
                opportunities.append({
                    'area': 'Position Improvement',
                    'description': f"Average position underperforming industry standard ({benchmarks['avg_position']})",
                    'action': 'Focus on technical SEO, content quality, and backlink profile'
                })
            elif metric == 'ctr':
                opportunities.append({
                    'area': 'CTR Optimization',
                    'description': f"CTR below industry average ({benchmarks['avg_ctr']['overall']}%)",
                    'action': 'Optimize title tags, meta descriptions, and rich snippets'
                })
            elif metric == 'mobile':
                opportunities.append({
                    'area': 'Mobile Optimization',
                    'description': f"Mobile traffic differs from industry norm ({benchmarks['mobile_percentage']}%)",
                    'action': 'Review mobile user experience and mobile-specific content'
                })

        return opportunities


# Global instance for easy import
competitive_benchmarks = CompetitiveBenchmarks()
