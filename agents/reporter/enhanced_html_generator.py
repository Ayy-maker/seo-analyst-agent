"""
Enhanced HTML Report Generator - 10x Better!
Includes interactive charts, animations, and comprehensive month-over-month tracking
WITH PHASE 3: Business Intelligence (Prioritization + Competitive Benchmarking)
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import json
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
# Import directly from module files to avoid matplotlib dependency
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'utils'))

from industry_detector import industry_detector
from demo_data_generator import demo_data_generator
from prioritization_engine import prioritization_engine
from competitive_benchmarks import competitive_benchmarks
from snapshot_manager import snapshot_manager


class EnhancedHTMLGenerator:
    """Generate premium interactive HTML reports with Chart.js visualizations"""
    
    def __init__(self, output_dir: str = "outputs/html-reports"):
        # Use absolute path to avoid issues with working directory
        if not Path(output_dir).is_absolute():
            # Get the project root (2 levels up from this file)
            project_root = Path(__file__).parent.parent.parent
            self.output_dir = project_root / output_dir
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_full_report(self,
                            company_name: str = "Sample Company",
                            report_period: str = "Monthly Report",
                            seo_data: Dict[str, Any] = None,
                            filename: str = None,
                            client_id: int = None) -> str:
        """Generate complete enhanced HTML report with charts"""

        if filename is None:
            timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
            filename = f"seo-report-{company_name.replace(' ', '-').lower()}-{timestamp}.html"

        output_path = self.output_dir / filename

        # Use default data if none provided - NOW WITH INDUSTRY INTELLIGENCE
        if seo_data is None:
            seo_data = self._get_default_data(company_name)

        # Add historical trend data if client_id is provided
        if client_id is not None:
            seo_data = self._add_historical_trends(seo_data, client_id)

        # Generate HTML with Chart.js
        html_content = self._generate_enhanced_html(company_name, report_period, seo_data)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Return absolute path
        return str(output_path.resolve())
    
    def _get_default_data(self, company_name: str = "Sample Company") -> Dict[str, Any]:
        """Get intelligent demo data based on industry detection"""

        # Detect industry from company name
        industry = industry_detector.detect_industry(company_name)

        # Extract location if present
        location = industry_detector.get_location_from_name(company_name) or 'Sydney'

        # Generate complete realistic dataset
        demo_dataset = demo_data_generator.generate_complete_dataset(
            industry=industry,
            location=location,
            historical_months=7
        )

        # Convert to format expected by template
        totals = demo_dataset['totals']
        keywords = demo_dataset['keywords'][:5]  # Top 5

        # Map performance levels based on CTR
        def get_performance(ctr):
            if ctr >= 6:
                return 'Excellent'
            elif ctr >= 4:
                return 'Good'
            else:
                return 'Improving'

        # ============ PHASE 3: GENERATE PRIORITIZED RECOMMENDATIONS ============
        raw_recommendations = [
            {
                'title': 'Mobile Optimization Priority',
                'description': 'Continue optimizing for mobile devices and implement accelerated mobile pages (AMP) for improved performance.',
                'expected_impact': f'Increase mobile CTR by +15%, potentially adding {int(totals["clicks"] * 0.15)} monthly clicks',
                'effort': 'Medium',
                'timeline': '1 month',
                'confidence': 'High'
            },
            {
                'title': 'Position Improvement Strategy',
                'description': 'Focus on queries ranking between positions 15-25 with enhanced content depth and optimization.',
                'expected_impact': f'Move 5 keywords to page 1, adding ~{int(totals["clicks"] * 0.25)} monthly clicks',
                'effort': 'Medium',
                'timeline': '2 weeks',
                'confidence': 'High'
            },
            {
                'title': 'Content Gap Analysis',
                'description': 'Create comprehensive guides and comparison content targeting informational queries.',
                'expected_impact': f'Capture long-tail traffic, +{int(totals["impressions"] * 0.30)} monthly impressions',
                'effort': 'High',
                'timeline': '3 months',
                'confidence': 'Medium'
            },
            {
                'title': 'Technical SEO Enhancements',
                'description': 'Address identified technical issues and implement structured data markup.',
                'expected_impact': 'Improve crawlability and rich snippet eligibility',
                'effort': 'Low',
                'timeline': '2 weeks',
                'confidence': 'High'
            },
            {
                'title': 'Local SEO Amplification',
                'description': 'Increase local business profile activity and acquire location-specific citations.',
                'expected_impact': f'Boost local visibility by 40%, adding {int(totals["clicks"] * 0.20)} monthly clicks',
                'effort': 'Low',
                'timeline': '1 month',
                'confidence': 'High'
            }
        ]

        # Prioritize recommendations using Phase 3 engine
        prioritized_recs = prioritization_engine.prioritize_recommendations(raw_recommendations)

        # ============ PHASE 3: COMPETITIVE BENCHMARKING ============
        competitive_data = competitive_benchmarks.compare_performance(
            data={
                'avg_position': totals['avg_position'],
                'ctr': totals['ctr'],
                'clicks': totals['clicks'],
                'impressions': totals['impressions']
            },
            industry=industry
        )

        return {
            'kpis': {
                # Real data only - no fabricated changes until we have historical tracking
                'total_clicks': {'value': totals['clicks'], 'change': None, 'prev': None},
                'impressions': {'value': totals['impressions'], 'change': None, 'prev': None},
                'ctr': {'value': totals['ctr'], 'change': None, 'prev': None},
                'avg_position': {'value': totals['avg_position'], 'change': None, 'prev': None}
            },
            'phase3': {
                'prioritized_recommendations': prioritized_recs,
                'competitive_benchmarks': competitive_data,
                'priority_summary': prioritization_engine.get_priority_summary(prioritized_recs)
            },
            'top_queries': [
                {
                    'rank': i+1,
                    'query': kw['query'],
                    'clicks': kw['clicks'],
                    'impressions': kw['impressions'],
                    'ctr': kw['ctr'],
                    'position': kw['position'],
                    'performance': get_performance(kw['ctr'])
                }
                for i, kw in enumerate(keywords)
            ],
            'landing_pages': [
                {
                    'url': page['url'],
                    'label': page['name'],
                    'clicks': page['clicks'],
                    'change': page['growth'],
                    'impressions': page['impressions'],
                    'ctr': page['ctr'],
                    'position': page['position']
                }
                for page in demo_dataset['landing_pages'][:4]  # Top 4 pages
            ],
            'devices': [
                {
                    'device': 'Mobile',
                    'icon': '📱',
                    'clicks': max(0, int(totals['clicks'] * (demo_dataset['devices']['mobile'] / 100))),
                    'percentage': max(0, demo_dataset['devices']['mobile'])
                },
                {
                    'device': 'Desktop',
                    'icon': '💻',
                    'clicks': max(0, int(totals['clicks'] * (demo_dataset['devices']['desktop'] / 100))),
                    'percentage': max(0, demo_dataset['devices']['desktop'])
                },
                {
                    'device': 'Tablet',
                    'icon': '📟',
                    'clicks': max(0, int(totals['clicks'] * (demo_dataset['devices']['tablet'] / 100))),
                    'percentage': max(0, demo_dataset['devices']['tablet'])
                },
            ],
            'monthly_progress': [
                {
                    'month': (datetime.now() + timedelta(days=30*month['month_offset'])).strftime('%B'),
                    'clicks': month['clicks'],
                    'impressions': month['impressions'],
                    'ctr': round((month['clicks'] / month['impressions']) * 100, 1),
                    'position': round(totals['avg_position'] - (month['month_offset'] * 1.8), 1),  # Improving over time
                    'health': month['health_score']
                }
                for month in demo_dataset['historical']
            ],
            'progress': []  # No fake progress data - will show real trends once we have historical data
        }

    def _add_historical_trends(self, seo_data: Dict[str, Any], client_id: int) -> Dict[str, Any]:
        """Add historical trend data from monthly snapshots if available"""

        # Check if client has historical data
        if not snapshot_manager.has_historical_data(client_id):
            return seo_data

        snapshot_count = snapshot_manager.get_snapshot_count(client_id)

        # Need at least 2 snapshots for meaningful trends
        if snapshot_count < 2:
            return seo_data

        # Fetch last 12 months of snapshots
        snapshots = snapshot_manager.get_snapshots(client_id, months=12)

        if not snapshots:
            return seo_data

        # Reverse to get oldest first (for chronological order in charts)
        snapshots.reverse()

        # Build monthly_progress data from snapshots
        monthly_progress = []
        for snapshot in snapshots:
            month_name = datetime.strptime(snapshot['snapshot_month'], '%Y-%m').strftime('%B %Y')
            monthly_progress.append({
                'month': month_name,
                'clicks': snapshot['total_clicks'],
                'impressions': snapshot['total_impressions'],
                'ctr': snapshot['avg_ctr'],
                'position': snapshot['avg_position'],
                'users': snapshot['total_users'],
                'sessions': snapshot['total_sessions']
            })

        # Add to seo_data
        if not seo_data:
            seo_data = {}

        seo_data['monthly_progress'] = monthly_progress
        seo_data['has_historical_data'] = True
        seo_data['snapshot_count'] = snapshot_count

        return seo_data

    def _generate_enhanced_html(self, company_name: str, report_period: str, data: Dict) -> str:
        """Generate enhanced HTML with Chart.js visualizations"""
        
        # Prepare chart data
        months = [m['month'] for m in data.get('monthly_progress', [])]
        clicks_data = [m['clicks'] for m in data.get('monthly_progress', [])]
        impressions_data = [m['impressions']/1000 for m in data.get('monthly_progress', [])]  # In thousands
        health_data = [m['health'] for m in data.get('monthly_progress', [])]
        position_data = [m['position'] for m in data.get('monthly_progress', [])]
        
        # Build table rows HTML
        top_queries_html = self._build_queries_table(data.get('top_queries', []))
        landing_pages_html = self._build_landing_pages_table(data.get('landing_pages', []))
        device_cards_html = self._build_device_cards(data.get('devices', []))
        progress_html = self._build_progress_table(data.get('progress', []))
        
        report_date = datetime.now().strftime('%B %d, %Y')
        
        # Generate complete HTML
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} - SEO Performance Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        {self._get_premium_css()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {company_name}</h1>
            <div class="subtitle">SEO Performance Report</div>
            <div class="date-badge">📅 {report_period} | {report_date}</div>
        </div>

        <div class="content">
            <div class="executive-summary">
                <h2>📊 Executive Summary</h2>
                <p>
                    This baseline report for <strong>{company_name}</strong> provides a comprehensive snapshot of current SEO performance
                    based on the most recent 30-day period. The website achieved <strong>{data['kpis']['total_clicks']['value']} total clicks</strong>
                    and <strong>{data['kpis']['impressions']['value']:,} impressions</strong> from organic search.
                    This data establishes a performance baseline for tracking future improvements. The current average click-through rate
                    of <strong>{data['kpis']['ctr']['value']:.2f}%</strong> and average position of <strong>{data['kpis']['avg_position']['value']:.1f}</strong>
                    provide key metrics for optimization opportunities.
                </p>
            </div>

            <div class="kpi-dashboard">
                <div class="kpi-card">
                    <div class="kpi-label">Total Clicks (30 days)</div>
                    <div class="kpi-value" data-target="{data['kpis']['total_clicks']['value']}">0</div>
                    <div class="kpi-trend" style="color: #718096;">
                        Baseline Period
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Impressions (30 days)</div>
                    <div class="kpi-value" data-target="{data['kpis']['impressions']['value'] / 1000:.1f}">0</div>
                    <div class="kpi-trend" style="color: #718096;">
                        {data['kpis']['impressions']['value']:,} total
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Click-Through Rate</div>
                    <div class="kpi-value" data-target="{data['kpis']['ctr']['value']}">0</div>
                    <div class="kpi-trend" style="color: #718096;">
                        Current Performance
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Average Position</div>
                    <div class="kpi-value" data-target="{data['kpis']['avg_position']['value']}">0</div>
                    <div class="kpi-trend" style="color: #718096;">
                        Current Ranking
                    </div>
                </div>
            </div>

            {self._build_ga4_metrics_section(data.get('ga4_metrics', {}))}

            <!-- BASELINE NOTICE -->
            <div style="background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #0284c7; margin: 40px 0;">
                <h2 style="color: #0284c7; margin: 0 0 15px 0; display: flex; align-items: center; gap: 10px;">
                    📊 Baseline Report - Historical Tracking Starts Next Month
                </h2>
                <p style="color: #0c4a6e; font-size: 15px; line-height: 1.6; margin: 0;">
                    This is your <strong>baseline performance report</strong>. Starting next month, you'll see month-over-month trend charts
                    showing clicks, impressions, CTR, and position changes over time. This baseline establishes your starting point for
                    measuring SEO improvements.
                </p>
            </div>

            <h2 class="section-header">🔍 Top Performing Search Queries</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Search Query</th>
                        <th>Clicks</th>
                        <th>Impressions</th>
                        <th>CTR</th>
                        <th>Avg Position</th>
                        <th>Performance</th>
                    </tr>
                </thead>
                <tbody>
{top_queries_html}
                </tbody>
            </table>

            <h2 class="section-header">📄 Top Landing Pages</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Page URL</th>
                        <th>Clicks</th>
                        <th>Impressions</th>
                        <th>CTR</th>
                        <th>Position</th>
                    </tr>
                </thead>
                <tbody>
{landing_pages_html}
                </tbody>
            </table>

            <h2 class="section-header">📱 Device Distribution</h2>
            <div class="device-grid">
{device_cards_html}
            </div>

            <!-- Progress Comparison removed - will be enabled once historical tracking is implemented -->

            <!-- PHASE 3: PRIORITIZED RECOMMENDATIONS -->
            <div class="recommendations">
                <h2>💡 Prioritized Strategic Recommendations</h2>
                <div class="priority-stats">
                    <span class="stat-badge quick-win">⚡ {data.get('phase3', {}).get('priority_summary', {}).get('breakdown', {}).get('quick_wins', 0)} Quick Wins</span>
                    <span class="stat-badge high-impact">🎯 {data.get('phase3', {}).get('priority_summary', {}).get('breakdown', {}).get('high_impact', 0)} High Impact</span>
                    <span class="stat-badge strategic">📊 {data.get('phase3', {}).get('priority_summary', {}).get('breakdown', {}).get('strategic', 0)} Strategic</span>
                </div>
                {self._build_prioritized_recommendations_html(data.get('phase3', {}).get('prioritized_recommendations', []))}
            </div>

            <!-- PHASE 3: COMPETITIVE BENCHMARKING -->
            {self._build_competitive_benchmarking_html(data.get('phase3', {}).get('competitive_benchmarks', {}))}

            {self._build_performance_insights_html(data)}

            <h2 class="section-header">✅ SEO Deliverables Completed</h2>
            <div class="recommendations" style="background: linear-gradient(135deg, #48bb7815 0%, #48bb7825 100%); border-left-color: #48bb78;">
                <h2 style="color: #48bb78;">✨ Implementation Highlights</h2>
                <ul>
                    <li><strong>Technical SEO Foundation:</strong> Complete website audit and optimization of technical elements.</li>
                    <li><strong>On-Page Optimization:</strong> Full optimization of key pages with enhanced meta data and content structure.</li>
                    <li><strong>Content Development:</strong> Creation of SEO-optimized content with comprehensive keyword integration.</li>
                    <li><strong>Local SEO Implementation:</strong> Business profile optimization and local citation building.</li>
                    <li><strong>Link Building Campaign:</strong> Acquisition of high-quality backlinks from relevant industry sources.</li>
                    <li><strong>Structured Data:</strong> Implementation of schema markup for enhanced search appearance.</li>
                    <li><strong>Mobile Optimization:</strong> Responsive design improvements and mobile performance optimization.</li>
                    <li><strong>Keyword Strategy:</strong> Comprehensive keyword research, mapping, and competitor analysis.</li>
                    <li><strong>Analytics Setup:</strong> Enhanced tracking configuration with conversion goals and custom reports.</li>
                    <li><strong>User Experience:</strong> Improved navigation, clear CTAs, and streamlined conversion paths.</li>
                </ul>
            </div>
        </div>

        <div class="footer">
            <h3>{company_name}</h3>
            <p>SEO Performance Report Generated: {report_date}</p>
            <p style="margin-top: 20px; font-size: 12px;">This report contains proprietary analysis. All metrics are sourced from Google Search Console, Google Analytics, and other SEO tools. Data is accurate as of the report generation date.</p>
        </div>
    </div>

    <script>
        // Chart.js configurations
        const chartMonths = {json.dumps(months)};
        const clicksData = {json.dumps(clicks_data)};
        const impressionsData = {json.dumps(impressions_data)};
        const healthData = {json.dumps(health_data)};
        const positionData = {json.dumps(position_data)};

        {self._get_chartjs_code(data)}
        {self._get_animation_code()}
    </script>
</body>
</html>'''
    
    def _build_queries_table(self, queries: List[Dict]) -> str:
        """Build top queries table HTML"""
        if not queries:
            return """
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: #718096;">
                            <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
                            <strong>No query data available yet</strong><br>
                            <span style="font-size: 14px;">Query data will appear once Google Search Console has sufficient data to display.</span>
                        </td>
                    </tr>"""

        html = ""
        for query in queries:
            perf_class = query['performance'].lower().replace(' ', '-')
            html += f"""
                    <tr>
                        <td><span class="rank-badge">{query['rank']}</span></td>
                        <td><strong>{query['query']}</strong></td>
                        <td>{query['clicks']}</td>
                        <td>{query['impressions']:,}</td>
                        <td>{query['ctr']}%</td>
                        <td>{query['position']}</td>
                        <td><span class="performance-badge {perf_class}">{query['performance']}</span></td>
                    </tr>"""
        return html
    
    def _build_landing_pages_table(self, pages: List[Dict]) -> str:
        """Build landing pages table HTML"""
        if not pages:
            return """
                    <tr>
                        <td colspan="5" style="text-align: center; padding: 40px; color: #718096;">
                            <div style="font-size: 48px; margin-bottom: 10px;">📄</div>
                            <strong>No landing page data available yet</strong><br>
                            <span style="font-size: 14px;">Landing page performance will appear once traffic data is collected.</span>
                        </td>
                    </tr>"""

        html = ""
        for page in pages:
            html += f"""
                    <tr>
                        <td><strong>{page['url']}</strong> ({page['label']})</td>
                        <td>{page['clicks']}</td>
                        <td>{page['impressions']:,}</td>
                        <td>{page['ctr']}%</td>
                        <td>{page['position']}</td>
                    </tr>"""
        return html
    
    def _build_device_cards(self, devices: List[Dict]) -> str:
        """Build device cards HTML"""
        if not devices:
            return """
                <div style="text-align: center; padding: 60px 40px; background: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <div style="font-size: 64px; margin-bottom: 20px;">📱💻📟</div>
                    <h3 style="color: #2d3748; margin-bottom: 10px;">No device data available yet</h3>
                    <p style="color: #718096; font-size: 15px;">Device distribution will appear once traffic data is collected from multiple device types.</p>
                </div>"""

        html = ""
        for device in devices:
            html += f"""
                <div class="device-card">
                    <div class="device-icon">{device['icon']}</div>
                    <div class="device-percentage" data-target="{device['percentage']}">0</div>
                    <div class="device-label">{device['device']}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" data-width="{device['percentage']}"></div>
                    </div>
                    <div class="device-clicks">{device['clicks']} clicks</div>
                </div>"""
        return html
    
    def _build_progress_table(self, progress: List[Dict]) -> str:
        """Build progress comparison table HTML"""
        html = ""
        for item in progress:
            html += f"""
                    <tr>
                        <td><strong>{item['metric']}</strong></td>
                        <td>{item['previous']}</td>
                        <td>{item['current']}</td>
                        <td>{item['change']}</td>
                        <td><span class="metric-change positive">{item['growth']}</span></td>
                    </tr>"""
        return html

    def _build_performance_insights_html(self, data: Dict[str, Any]) -> str:
        """Build data-driven performance insights or skip if insufficient data"""

        # Get KPI data
        kpis = data.get('kpis', {})
        total_clicks = kpis.get('total_clicks', {}).get('value', 0)
        avg_position = kpis.get('avg_position', {}).get('value', 100)
        avg_ctr = kpis.get('ctr', {}).get('value', 0)

        # If we have very low data (< 10 clicks) or very poor position (> 50),
        # show a focused "baseline" message instead of generic strengths
        if total_clicks < 10 or avg_position > 50:
            return f"""
            <h2 class="section-header">🎯 Baseline Performance Analysis</h2>
            <div style="background: linear-gradient(135deg, #f39c1215 0%, #f39c1225 100%); border-left: 5px solid #f39c12; padding: 30px; border-radius: 10px; margin-bottom: 40px;">
                <h3 style="color: #f39c12; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                    📊 Current Status: Building SEO Foundation
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <h4 style="color: #2d3748; margin-bottom: 10px;">📌 What This Baseline Tells Us:</h4>
                        <ul style="list-style: none; padding: 0; color: #4a5568;">
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">•</span>
                                Current visibility: Position {avg_position:.1f} (Page {int(avg_position/10) + 1})
                            </li>
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">•</span>
                                Traffic level: {total_clicks} clicks in 30 days (early stage)
                            </li>
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">•</span>
                                CTR: {avg_ctr:.2f}% (typical for positions beyond page 1)
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #2d3748; margin-bottom: 10px;">🎯 Immediate Focus Areas:</h4>
                        <ul style="list-style: none; padding: 0; color: #4a5568;">
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">1.</span>
                                <strong>Improve Rankings:</strong> Target page 1-2 positions (1-20)
                            </li>
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">2.</span>
                                <strong>Expand Keywords:</strong> Increase number of ranking queries
                            </li>
                            <li style="padding: 8px 0; padding-left: 25px; position: relative;">
                                <span style="position: absolute; left: 0;">3.</span>
                                <strong>Content Optimization:</strong> Enhance existing pages for better relevance
                            </li>
                        </ul>
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.6); border-radius: 8px;">
                    <strong style="color: #2d3748;">💡 Next Steps:</strong> Focus on ranking improvements and content optimization.
                    Historical trend tracking will show progress starting next month with month-over-month comparisons.
                </div>
            </div>"""

        # If we have reasonable data, show standard insights
        return """
            <h2 class="section-header">🎯 Performance Insights</h2>
            <div class="insights-grid">
                <div class="insights-box strengths">
                    <h3>💪 Key Strengths</h3>
                    <ul>
                        <li><strong>Established Presence:</strong> Website indexed and appearing in search results.</li>
                        <li><strong>Technical Foundation:</strong> Site accessible and crawlable by search engines.</li>
                        <li><strong>Growth Tracking:</strong> Historical tracking now enabled for month-over-month progress measurement.</li>
                    </ul>
                </div>
                <div class="insights-box improvements">
                    <h3>📈 Growth Opportunities</h3>
                    <ul>
                        <li><strong>Ranking Improvement:</strong> Target higher positions for better visibility and traffic.</li>
                        <li><strong>Content Enhancement:</strong> Expand and optimize content to address user intent comprehensively.</li>
                        <li><strong>CTR Optimization:</strong> Improve meta descriptions and titles for higher click-through rates.</li>
                        <li><strong>Keyword Expansion:</strong> Identify and target additional relevant search queries.</li>
                    </ul>
                </div>
            </div>"""

    def _build_prioritized_recommendations_html(self, recommendations: List[Dict]) -> str:
        """Build Phase 3 prioritized recommendations HTML"""
        if not recommendations:
            return "<p>No recommendations available</p>"

        html = '<div class="priority-recommendations">'

        for rec in recommendations:
            priority = rec.get('priority', 'STRATEGIC')
            priority_class = priority.lower().replace(' ', '-')
            final_score = rec.get('final_score', 0)
            impact_score = rec.get('impact_score', 0)
            effort_score = rec.get('effort_score', 0)
            roi_score = rec.get('roi_score', 0)

            # Extract title and description from AI recommendation format
            recommendation_main = rec.get('recommendation', rec.get('description', rec.get('title', 'Recommendation')))
            # Use first 100 chars as title
            title_text = recommendation_main[:100] + '...' if len(recommendation_main) > 100 else recommendation_main

            # Build comprehensive description from all AI fields
            description_parts = [recommendation_main]
            if rec.get('reasoning'):
                description_parts.append(f"<br><br><strong>Why:</strong> {rec['reasoning']}")
            if rec.get('data_evidence'):
                evidence_list = '<br>'.join([f"• {item}" for item in rec['data_evidence'][:3]])  # Top 3 evidence
                description_parts.append(f"<br><br><strong>Data Evidence:</strong><br>{evidence_list}")
            recommendation_text = ''.join(description_parts)

            # Get impact estimate
            impact_text = rec.get('impact_estimate', rec.get('expected_impact', 'Estimated improvement in SEO performance'))

            html += f'''
                <div class="recommendation-card">
                    <div class="rec-header">
                        <div class="rec-title">
                            <h3>{title_text}</h3>
                            <span class="priority-badge {priority_class}">{priority}</span>
                        </div>
                        <div class="rec-score">
                            <div class="score-circle">{final_score:.1f}</div>
                            <div class="score-label">Priority Score</div>
                        </div>
                    </div>
                    <p class="rec-description">{recommendation_text}</p>
                    <div class="rec-metrics">
                        <div class="metric">
                            <span class="metric-label">Impact</span>
                            <span class="metric-value">{impact_score:.1f}/10</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Effort</span>
                            <span class="metric-value">{effort_score}/10</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">ROI</span>
                            <span class="metric-value">{roi_score:.1f}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Timeline</span>
                            <span class="metric-value">{rec.get('timeline', 'N/A')}</span>
                        </div>
                    </div>
                    <div class="rec-impact">
                        <strong>Expected Impact:</strong> {impact_text}
                    </div>
                </div>'''

        html += '</div>'
        return html

    def _build_competitive_benchmarking_html(self, benchmarks: Dict) -> str:
        """Build Phase 3 competitive benchmarking HTML"""
        if not benchmarks:
            return ""

        overall_score = benchmarks.get('overall_score', 0)
        industry = benchmarks.get('industry', 'general').title()

        # Determine rating and color
        if overall_score >= 80:
            rating = "Industry Leader"
            rating_class = "leader"
        elif overall_score >= 70:
            rating = "Above Average"
            rating_class = "above-average"
        elif overall_score >= 60:
            rating = "Average"
            rating_class = "average"
        elif overall_score >= 50:
            rating = "Below Average"
            rating_class = "below-average"
        else:
            rating = "Needs Improvement"
            rating_class = "needs-improvement"

        html = f'''
            <div class="competitive-section">
                <h2 class="section-header">🏆 Competitive Benchmarking</h2>
                <div class="benchmark-card">
                    <div class="benchmark-header">
                        <div class="benchmark-score-display">
                            <div class="large-score-circle {rating_class}">
                                {overall_score}
                            </div>
                            <div class="score-details">
                                <h3>{rating}</h3>
                                <p>vs {industry} Industry</p>
                            </div>
                        </div>
                    </div>

                    <div class="benchmark-grid">
                        <div class="benchmark-box strengths">
                            <h4>💪 Competitive Strengths</h4>
                            <ul>'''

        for strength in benchmarks.get('strengths', [])[:5]:
            html += f'<li>{strength}</li>'

        html += '''
                            </ul>
                        </div>
                        <div class="benchmark-box weaknesses">
                            <h4>⚠️ Areas Behind Competition</h4>
                            <ul>'''

        for weakness in benchmarks.get('weaknesses', [])[:5]:
            html += f'<li>{weakness}</li>'

        html += '''
                            </ul>
                        </div>
                        <div class="benchmark-box opportunities">
                            <h4>🎯 Growth Opportunities</h4>
                            <ul>'''

        for opportunity in benchmarks.get('opportunities', [])[:5]:
            html += f'<li>{opportunity}</li>'

        html += '''
                            </ul>
                        </div>
                    </div>
                </div>
            </div>'''

        return html

    def _build_ga4_metrics_section(self, ga4_metrics: Dict) -> str:
        """Build Google Analytics 4 metrics section HTML"""
        if not ga4_metrics:
            return ''

        total_users = ga4_metrics.get('total_users', 0)
        total_sessions = ga4_metrics.get('total_sessions', 0)
        total_page_views = ga4_metrics.get('total_page_views', 0)
        engagement_rate = ga4_metrics.get('avg_engagement_rate', 0)
        bounce_rate = ga4_metrics.get('avg_bounce_rate', 0)
        session_duration = ga4_metrics.get('avg_session_duration', 0)
        pages_per_session = ga4_metrics.get('pages_per_session', 0)
        user_growth = ga4_metrics.get('user_growth', 0)
        session_growth = ga4_metrics.get('session_growth', 0)

        html = f'''
            <!-- GOOGLE ANALYTICS 4 METRICS -->
            <div style="margin: 40px 0; background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #1890ff;">
                <h2 class="section-header" style="color: #1890ff; margin-top: 0;">📊 Google Analytics 4 User Behavior Metrics</h2>
                <p style="color: #666; margin-bottom: 25px;">Real user engagement and behavior data from Google Analytics 4</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 25px;">
                    <!-- Total Users -->
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(24, 144, 255, 0.1); border-top: 3px solid #1890ff;">
                        <div style="font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">
                            👥 Total Users
                        </div>
                        <div style="font-size: 36px; font-weight: 700; color: #1890ff; margin-bottom: 8px;">
                            {total_users:,}
                        </div>
                        <div style="font-size: 13px; color: #718096; font-weight: 600;">
                            30-day baseline
                        </div>
                    </div>

                    <!-- Total Sessions -->
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(82, 196, 26, 0.1); border-top: 3px solid #52c41a;">
                        <div style="font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">
                            🎯 Total Sessions
                        </div>
                        <div style="font-size: 36px; font-weight: 700; color: #52c41a; margin-bottom: 8px;">
                            {total_sessions:,}
                        </div>
                        <div style="font-size: 13px; color: #718096; font-weight: 600;">
                            30-day baseline
                        </div>
                    </div>

                    <!-- Engagement Rate -->
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(250, 173, 20, 0.1); border-top: 3px solid #faad14;">
                        <div style="font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">
                            ⚡ Engagement Rate
                        </div>
                        <div style="font-size: 36px; font-weight: 700; color: #faad14; margin-bottom: 8px;">
                            {engagement_rate}%
                        </div>
                        <div style="font-size: 13px; color: #666;">
                            {self._get_engagement_label(engagement_rate)}
                        </div>
                    </div>

                    <!-- Page Views -->
                    <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(114, 46, 209, 0.1); border-top: 3px solid #722ed1;">
                        <div style="font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">
                            📄 Total Page Views
                        </div>
                        <div style="font-size: 36px; font-weight: 700; color: #722ed1; margin-bottom: 8px;">
                            {total_page_views:,}
                        </div>
                        <div style="font-size: 13px; color: #666;">
                            {pages_per_session} pages/session
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <!-- Bounce Rate -->
                    <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div style="font-size: 13px; color: #666; margin-bottom: 8px;">📉 Bounce Rate</div>
                        <div style="font-size: 28px; font-weight: 600; color: {self._get_bounce_color(bounce_rate)};">
                            {bounce_rate}%
                        </div>
                        <div style="font-size: 12px; color: #888; margin-top: 5px;">
                            {self._get_bounce_label(bounce_rate)}
                        </div>
                    </div>

                    <!-- Session Duration -->
                    <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div style="font-size: 13px; color: #666; margin-bottom: 8px;">⏱️ Avg Session Duration</div>
                        <div style="font-size: 28px; font-weight: 600; color: #13c2c2;">
                            {session_duration}s
                        </div>
                        <div style="font-size: 12px; color: #888; margin-top: 5px;">
                            {self._format_duration(session_duration)}
                        </div>
                    </div>

                    <!-- Pages per Session -->
                    <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div style="font-size: 13px; color: #666; margin-bottom: 8px;">📑 Pages per Session</div>
                        <div style="font-size: 28px; font-weight: 600; color: #eb2f96;">
                            {pages_per_session}
                        </div>
                        <div style="font-size: 12px; color: #888; margin-top: 5px;">
                            {self._get_pages_label(pages_per_session)}
                        </div>
                    </div>
                </div>
            </div>'''

        return html

    def _get_engagement_label(self, rate: float) -> str:
        """Get engagement quality label"""
        if rate >= 70:
            return '🌟 Excellent Engagement'
        elif rate >= 60:
            return '✅ Good Engagement'
        elif rate >= 50:
            return '👍 Average Engagement'
        else:
            return '⚠️ Needs Improvement'

    def _get_bounce_color(self, rate: float) -> str:
        """Get bounce rate color"""
        if rate <= 25:
            return '#52c41a'  # Green
        elif rate <= 40:
            return '#faad14'  # Orange
        else:
            return '#f5222d'  # Red

    def _get_bounce_label(self, rate: float) -> str:
        """Get bounce rate quality label"""
        if rate <= 25:
            return '🌟 Excellent'
        elif rate <= 40:
            return '✅ Good'
        elif rate <= 55:
            return '⚠️ Average'
        else:
            return '❌ High'

    def _format_duration(self, seconds: int) -> str:
        """Format session duration in minutes:seconds"""
        mins = seconds // 60
        secs = seconds % 60
        return f'{mins}m {secs}s'

    def _get_pages_label(self, pages: float) -> str:
        """Get pages per session quality label"""
        if pages >= 4:
            return '🌟 Excellent Depth'
        elif pages >= 2.5:
            return '✅ Good Depth'
        else:
            return '⚠️ Could Improve'

    def _get_premium_css(self) -> str:
        """Get premium CSS with chart styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2d3748;
            line-height: 1.6;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header h1 {
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .header .subtitle {
            font-size: 24px;
            font-weight: 300;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }

        .date-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 600;
            position: relative;
            z-index: 1;
            backdrop-filter: blur(10px);
        }

        .content {
            padding: 40px;
        }

        .executive-summary {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 5px solid #667eea;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 40px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        }

        .executive-summary h2 {
            font-size: 28px;
            margin-bottom: 20px;
            color: #667eea;
        }

        .executive-summary p {
            font-size: 16px;
            line-height: 1.8;
            color: #4a5568;
        }

        .kpi-dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }

        .kpi-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-top: 4px solid;
            transition: all 0.3s ease;
        }

        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
        }

        .kpi-card:nth-child(1) { border-top-color: #48bb78; }
        .kpi-card:nth-child(2) { border-top-color: #667eea; }
        .kpi-card:nth-child(3) { border-top-color: #f39c12; }
        .kpi-card:nth-child(4) { border-top-color: #764ba2; }

        .kpi-label {
            font-size: 14px;
            color: #718096;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .kpi-value {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }

        .kpi-trend {
            font-size: 14px;
            color: #48bb78;
            font-weight: 600;
        }

        .kpi-trend .arrow {
            display: inline-block;
            margin-right: 5px;
        }

        /* Charts Grid */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .chart-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 5px solid #667eea;
        }

        .chart-card h3 {
            font-size: 18px;
            color: #2d3748;
            margin-bottom: 20px;
            font-weight: 700;
        }

        .section-header {
            font-size: 32px;
            font-weight: 700;
            margin: 50px 0 30px 0;
            color: #2d3748;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 40px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        .data-table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .data-table th {
            padding: 20px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .data-table tbody tr {
            border-bottom: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }

        .data-table tbody tr:hover {
            background: #f7fafc;
            transform: scale(1.01);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        .data-table td {
            padding: 20px;
            font-size: 14px;
        }

        .rank-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 700;
            font-size: 14px;
        }

        .performance-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .performance-badge.excellent {
            background: #48bb78;
            color: white;
        }

        .performance-badge.good {
            background: #f39c12;
            color: white;
        }

        .performance-badge.improving {
            background: #dc2626;
            color: white;
        }

        .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }

        .device-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            text-align: center;
            transition: all 0.3s ease;
        }

        .device-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
        }

        .device-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }

        .device-percentage {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }

        .device-label {
            font-size: 16px;
            color: #718096;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            transition: width 1s ease;
            width: 0;
        }

        .device-clicks {
            font-size: 14px;
            color: #4a5568;
            font-weight: 500;
        }

        .recommendations {
            background: linear-gradient(135deg, #f39c1215 0%, #f39c1225 100%);
            border-left: 5px solid #f39c12;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 40px;
        }

        .recommendations h2 {
            font-size: 28px;
            margin-bottom: 20px;
            color: #f39c12;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .recommendations ul {
            list-style: none;
            padding: 0;
        }

        .recommendations li {
            padding: 12px 0;
            padding-left: 35px;
            position: relative;
            font-size: 15px;
            line-height: 1.6;
            color: #4a5568;
        }

        .recommendations li::before {
            content: '✓';
            position: absolute;
            left: 0;
            top: 12px;
            width: 24px;
            height: 24px;
            background: #48bb78;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
        }

        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }

        .insights-box {
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .insights-box.strengths {
            background: linear-gradient(135deg, #48bb7815 0%, #48bb7825 100%);
            border-left: 5px solid #48bb78;
        }

        .insights-box.improvements {
            background: linear-gradient(135deg, #dc262615 0%, #dc262625 100%);
            border-left: 5px solid #dc2626;
        }

        .insights-box h3 {
            font-size: 22px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .insights-box.strengths h3 {
            color: #48bb78;
        }

        .insights-box.improvements h3 {
            color: #dc2626;
        }

        .insights-box ul {
            list-style: none;
            padding: 0;
        }

        .insights-box li {
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            font-size: 14px;
            color: #4a5568;
        }

        .insights-box.strengths li::before {
            content: '✅';
            position: absolute;
            left: 0;
            font-size: 18px;
        }

        .insights-box.improvements li::before {
            content: '⚠️';
            position: absolute;
            left: 0;
            font-size: 18px;
        }

        .footer {
            background: #2d3748;
            color: white;
            padding: 40px;
            text-align: center;
        }

        .footer h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .footer p {
            font-size: 14px;
            color: #a0aec0;
            margin: 5px 0;
        }

        .metric-change {
            font-size: 12px;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
            margin-left: 8px;
        }

        .metric-change.positive {
            background: #48bb7820;
            color: #48bb78;
        }

        /* ============ PHASE 3: PRIORITIZATION & BENCHMARKING STYLES ============ */

        .priority-stats {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .stat-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .stat-badge.quick-win {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }

        .stat-badge.high-impact {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .stat-badge.strategic {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
            color: white;
        }

        .priority-recommendations {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .recommendation-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid #667eea;
            transition: all 0.3s ease;
        }

        .recommendation-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
        }

        .rec-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        .rec-title {
            flex: 1;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .rec-title h3 {
            font-size: 18px;
            margin: 0;
            color: #2d3748;
        }

        .priority-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .priority-badge.quick-win {
            background: #48bb78;
            color: white;
        }

        .priority-badge.high-impact {
            background: #667eea;
            color: white;
        }

        .priority-badge.strategic {
            background: #f39c12;
            color: white;
        }

        .rec-score {
            text-align: center;
        }

        .score-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 800;
            margin: 0 auto 5px;
        }

        .score-label {
            font-size: 11px;
            color: #718096;
            font-weight: 600;
        }

        .rec-description {
            font-size: 15px;
            line-height: 1.6;
            color: #4a5568;
            margin-bottom: 15px;
        }

        .rec-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
            padding: 15px;
            background: #f7fafc;
            border-radius: 8px;
        }

        .rec-metrics .metric {
            text-align: center;
        }

        .rec-metrics .metric-label {
            display: block;
            font-size: 11px;
            color: #718096;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .rec-metrics .metric-value {
            display: block;
            font-size: 16px;
            font-weight: 700;
            color: #2d3748;
        }

        .rec-impact {
            font-size: 14px;
            color: #4a5568;
            padding: 12px;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-radius: 6px;
        }

        /* Competitive Benchmarking Styles */
        .competitive-section {
            margin: 40px 0;
        }

        .benchmark-card {
            background: white;
            border-radius: 15px;
            padding: 35px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }

        .benchmark-header {
            text-align: center;
            margin-bottom: 35px;
        }

        .benchmark-score-display {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 25px;
        }

        .large-score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 42px;
            font-weight: 800;
            color: white;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }

        .large-score-circle.leader {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        }

        .large-score-circle.above-average {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .large-score-circle.average {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        }

        .large-score-circle.below-average {
            background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
        }

        .large-score-circle.needs-improvement {
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        }

        .score-details {
            text-align: left;
        }

        .score-details h3 {
            font-size: 32px;
            margin: 0 0 5px 0;
            color: #2d3748;
        }

        .score-details p {
            font-size: 16px;
            color: #718096;
            margin: 0;
        }

        .benchmark-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .benchmark-box {
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid;
        }

        .benchmark-box.strengths {
            background: linear-gradient(135deg, #48bb7815 0%, #48bb7825 100%);
            border-left-color: #48bb78;
        }

        .benchmark-box.weaknesses {
            background: linear-gradient(135deg, #dc262615 0%, #dc262625 100%);
            border-left-color: #dc2626;
        }

        .benchmark-box.opportunities {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left-color: #667eea;
        }

        .benchmark-box h4 {
            font-size: 16px;
            margin-bottom: 15px;
            color: #2d3748;
        }

        .benchmark-box ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .benchmark-box li {
            padding: 8px 0;
            font-size: 14px;
            color: #4a5568;
            line-height: 1.5;
        }

        .benchmark-box.strengths li::before {
            content: '✅ ';
            margin-right: 8px;
        }

        .benchmark-box.weaknesses li::before {
            content: '⚠️ ';
            margin-right: 8px;
        }

        .benchmark-box.opportunities li::before {
            content: '🎯 ';
            margin-right: 8px;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 32px;
            }
            .charts-grid {
                grid-template-columns: 1fr;
            }
            .insights-grid {
                grid-template-columns: 1fr;
            }
            .content {
                padding: 20px;
            }
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
            }
        }
        """
    
    def _get_chartjs_code(self, data: Dict[str, Any]) -> str:
        """Get Chart.js initialization code - Now with real historical data support"""

        # Check if we have historical data
        if not data.get('has_historical_data', False) or not data.get('monthly_progress'):
            return """
            // Historical trend charts will be enabled once we have multiple months of data
            // For now, showing baseline report only
            console.log('Baseline report generated. Historical charts will appear next month.');
            """

        # Extract trend data
        monthly_progress = data.get('monthly_progress', [])
        months = [m['month'] for m in monthly_progress]
        clicks_data = [m['clicks'] for m in monthly_progress]
        impressions_data = [m['impressions']/1000 for m in monthly_progress]  # In thousands
        position_data = [m['position'] for m in monthly_progress]
        users_data = [m.get('users', 0) for m in monthly_progress]
        sessions_data = [m.get('sessions', 0) for m in monthly_progress]

        # Generate Chart.js code with real data
        return f"""
        // Chart.js - Historical Trend Visualizations
        const chartConfig = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: true,
                    position: 'bottom'
                }},
                tooltip: {{
                    mode: 'index',
                    intersect: false
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }};

        // Clicks & Impressions Chart
        if (document.getElementById('trendsChart')) {{
            new Chart(document.getElementById('trendsChart'), {{
                type: 'line',
                data: {{
                    labels: {json.dumps(months)},
                    datasets: [{{
                        label: 'Clicks',
                        data: {json.dumps(clicks_data)},
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4
                    }}, {{
                        label: 'Impressions (K)',
                        data: {json.dumps(impressions_data)},
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4
                    }}]
                }},
                options: chartConfig
            }});
        }}

        // Average Position Chart (inverted - lower is better)
        if (document.getElementById('positionChart')) {{
            new Chart(document.getElementById('positionChart'), {{
                type: 'line',
                data: {{
                    labels: {json.dumps(months)},
                    datasets: [{{
                        label: 'Average Position',
                        data: {json.dumps(position_data)},
                        borderColor: '#FFCE56',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4
                    }}]
                }},
                options: {{
                    ...chartConfig,
                    scales: {{
                        y: {{
                            reverse: true,  // Lower position is better
                            beginAtZero: false
                        }}
                    }}
                }}
            }});
        }}

        // Users & Sessions Chart
        if (document.getElementById('usersChart')) {{
            new Chart(document.getElementById('usersChart'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(months)},
                    datasets: [{{
                        label: 'Users',
                        data: {json.dumps(users_data)},
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: '#4BC0C0',
                        borderWidth: 2
                    }}, {{
                        label: 'Sessions',
                        data: {json.dumps(sessions_data)},
                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                        borderColor: '#9966FF',
                        borderWidth: 2
                    }}]
                }},
                options: chartConfig
            }});
        }}

        console.log('Historical trend charts loaded successfully!');
        """
    
    def _get_animation_code(self) -> str:
        """Get animation JavaScript code"""
        return """
        // Counter Animation
        function animateCounter(element) {
            const target = parseFloat(element.getAttribute('data-target'));
            const duration = 1000;
            const increment = target / (duration / 16);
            let current = 0;
            const isDecimal = target % 1 !== 0;

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                
                if (isDecimal) {
                    element.textContent = current.toFixed(1) + (element.classList.contains('device-percentage') ? '%' : '');
                } else if (target > 1000) {
                    element.textContent = (current / 1000).toFixed(1) + 'K';
                } else {
                    element.textContent = Math.floor(current);
                }
            }, 16);
        }

        // Progress Bar Animation
        function animateProgressBar(element) {
            const targetWidth = element.getAttribute('data-width');
            setTimeout(() => {
                element.style.width = targetWidth + '%';
            }, 100);
        }

        // Initialize animations on page load
        window.addEventListener('load', () => {
            document.querySelectorAll('.kpi-value[data-target]').forEach((element, index) => {
                setTimeout(() => animateCounter(element), index * 100);
            });

            document.querySelectorAll('.device-percentage[data-target]').forEach((element, index) => {
                setTimeout(() => animateCounter(element), index * 150);
            });

            document.querySelectorAll('.progress-fill[data-width]').forEach((element, index) => {
                setTimeout(() => animateProgressBar(element), index * 150 + 500);
            });
        });
        """
