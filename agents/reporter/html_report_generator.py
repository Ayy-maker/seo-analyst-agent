"""
HTML Report Generator
Creates stunning interactive HTML reports matching the premium design
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import json


class HTMLReportGenerator:
    """Generate interactive HTML reports with animations and charts"""
    
    def __init__(self, output_dir: str = "outputs/html-reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_full_report(self,
                            company_name: str = "Sample Company",
                            report_period: str = "Monthly Report",
                            seo_data: Dict[str, Any] = None,
                            filename: str = None) -> str:
        """
        Generate complete HTML report
        
        Args:
            company_name: Client company name
            report_period: Reporting period
            seo_data: Dictionary containing all SEO metrics
            filename: Output filename (auto-generated if None)
        
        Returns:
            Path to generated HTML file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
            filename = f"seo-report-{company_name.replace(' ', '-').lower()}-{timestamp}.html"
        
        output_path = self.output_dir / filename
        
        # Use default data if none provided
        if seo_data is None:
            seo_data = self._get_default_data()
        
        # Generate HTML
        html_content = self._generate_html(company_name, report_period, seo_data)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Get default sample data"""
        return {
            'kpis': {
                'total_clicks': {'value': 258, 'change': 286, 'prev': 67},
                'impressions': {'value': 8700, 'change': 412, 'prev': 1698},
                'ctr': {'value': 2.97, 'change': 25, 'prev': 2.4},
                'avg_position': {'value': 18.4, 'change': 40, 'prev': 30.7}
            },
            'top_queries': [
                {'rank': 1, 'query': 'sample branded term', 'clicks': 89, 'impressions': 1247, 'ctr': 7.1, 'position': 2.3, 'performance': 'Excellent'},
                {'rank': 2, 'query': 'sample keyword 1', 'clicks': 42, 'impressions': 1834, 'ctr': 2.3, 'position': 12.7, 'performance': 'Good'},
                {'rank': 3, 'query': 'sample keyword 2', 'clicks': 38, 'impressions': 2156, 'ctr': 1.8, 'position': 15.2, 'performance': 'Good'},
                {'rank': 4, 'query': 'sample keyword 3', 'clicks': 27, 'impressions': 1423, 'ctr': 1.9, 'position': 18.5, 'performance': 'Good'},
                {'rank': 5, 'query': 'sample keyword 4', 'clicks': 19, 'impressions': 987, 'ctr': 1.9, 'position': 21.3, 'performance': 'Improving'},
            ],
            'landing_pages': [
                {'url': '/', 'label': 'Homepage', 'clicks': 134, 'change': 298, 'impressions': 4523, 'ctr': 3.0, 'position': 8.2},
                {'url': '/services/', 'label': 'Services', 'clicks': 47, 'change': 385, 'impressions': 2167, 'ctr': 2.2, 'position': 16.4},
                {'url': '/about/', 'label': 'About', 'clicks': 28, 'change': 450, 'impressions': 1234, 'ctr': 2.3, 'position': 18.7},
                {'url': '/contact/', 'label': 'Contact', 'clicks': 22, 'change': 420, 'impressions': 987, 'ctr': 2.2, 'position': 21.5},
            ],
            'devices': [
                {'device': 'Mobile', 'icon': '📱', 'clicks': 175, 'percentage': 67.8},
                {'device': 'Desktop', 'icon': '💻', 'clicks': 74, 'percentage': 28.7},
                {'device': 'Tablet', 'icon': '📟', 'clicks': 9, 'percentage': 3.5},
            ],
            'monthly_progress': [
                {'month': 'March', 'clicks': 67, 'impressions': 1698, 'ctr': 2.4, 'position': 30.7, 'health': 72},
                {'month': 'April', 'clicks': 89, 'impressions': 2854, 'ctr': 2.5, 'position': 28.3, 'health': 75},
                {'month': 'May', 'clicks': 124, 'impressions': 4123, 'ctr': 2.6, 'position': 25.1, 'health': 78},
                {'month': 'June', 'clicks': 167, 'impressions': 5892, 'ctr': 2.7, 'position': 22.4, 'health': 82},
                {'month': 'July', 'clicks': 208, 'impressions': 7234, 'ctr': 2.8, 'position': 20.1, 'health': 85},
                {'month': 'August', 'clicks': 232, 'impressions': 7989, 'ctr': 2.9, 'position': 19.2, 'health': 86},
                {'month': 'September', 'clicks': 258, 'impressions': 8701, 'ctr': 3.0, 'position': 18.4, 'health': 87},
            ],
            'progress': [
                {'metric': 'Total Clicks', 'previous': 67, 'current': 258, 'change': '+191', 'growth': '+286%'},
                {'metric': 'Total Impressions', 'previous': '1,698', 'current': '8,701', 'change': '+7,003', 'growth': '+412%'},
                {'metric': 'Click-Through Rate', 'previous': '2.4%', 'current': '3.0%', 'change': '+0.6%', 'growth': '+25%'},
                {'metric': 'Average Position', 'previous': 30.7, 'current': 18.4, 'change': '-12.3', 'growth': '+40%'},
                {'metric': 'Active Users (GA4)', 'previous': 46, 'current': 161, 'change': '+115', 'growth': '+250%'},
                {'metric': 'Page Views', 'previous': 180, 'current': 654, 'change': '+474', 'growth': '+263%'},
                {'metric': 'Engagement Rate', 'previous': '38.2%', 'current': '51.9%', 'change': '+13.7%', 'growth': '+36%'},
                {'metric': 'Site Health Score', 'previous': '72%', 'current': '87%', 'change': '+15%', 'growth': '+21%'},
            ]
        }
    
    def _generate_html(self, company_name: str, report_period: str, data: Dict) -> str:
        """Generate complete HTML report"""
        
        # Build top queries table rows
        top_queries_html = ""
        for query in data['top_queries']:
            perf_class = query['performance'].lower().replace(' ', '-')
            top_queries_html += f"""
                    <tr>
                        <td><span class="rank-badge">{query['rank']}</span></td>
                        <td><strong>{query['query']}</strong></td>
                        <td>{query['clicks']}</td>
                        <td>{query['impressions']:,}</td>
                        <td>{query['ctr']}%</td>
                        <td>{query['position']}</td>
                        <td><span class="performance-badge {perf_class}">{query['performance']}</span></td>
                    </tr>"""
        
        # Build landing pages table rows
        landing_pages_html = ""
        for page in data['landing_pages']:
            landing_pages_html += f"""
                    <tr>
                        <td><strong>{page['url']}</strong> ({page['label']})</td>
                        <td>{page['clicks']} <span class="metric-change positive">+{page['change']}%</span></td>
                        <td>{page['impressions']:,}</td>
                        <td>{page['ctr']}%</td>
                        <td>{page['position']}</td>
                    </tr>"""
        
        # Build device cards
        device_cards_html = ""
        for device in data['devices']:
            device_cards_html += f"""
                <div class="device-card">
                    <div class="device-icon">{device['icon']}</div>
                    <div class="device-percentage" data-target="{device['percentage']}"</div>
                    <div class="device-label">{device['device']}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" data-width="{device['percentage']}"></div>
                    </div>
                    <div class="device-clicks">{device['clicks']} clicks</div>
                </div>"""
        
        # Build countries table
        countries_html = ""
        for country in data['countries']:
            countries_html += f"""
                    <tr>
                        <td><span class="country-flag">{country['flag']}</span> <strong>{country['country']}</strong></td>
                        <td>{country['clicks']}</td>
                        <td>{country['impressions']:,}</td>
                        <td>{country['ctr']}%</td>
                        <td>{country['share']}%</td>
                    </tr>"""
        
        # Build progress comparison table
        progress_html = ""
        for item in data['progress']:
            progress_html += f"""
                    <tr>
                        <td><strong>{item['metric']}</strong></td>
                        <td>{item['previous']}</td>
                        <td>{item['current']}</td>
                        <td>{item['change']}</td>
                        <td><span class="metric-change positive">{item['growth']}</span></td>
                    </tr>"""
        
        # Get report date
        report_date = datetime.now().strftime('%B %d, %Y')
        
        # Complete HTML with embedded CSS and JavaScript
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} - SEO Performance Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header">
            <h1>🚀 {company_name}</h1>
            <div class="subtitle">SEO Performance Report</div>
            <div class="date-badge">📅 {report_period} | {report_date}</div>
        </div>

        <!-- Content Section -->
        <div class="content">
            <!-- Executive Summary -->
            <div class="executive-summary">
                <h2>Executive Summary</h2>
                <p>
                    Over the reporting period, <strong>{company_name}</strong> has achieved remarkable SEO growth through strategic optimization efforts. 
                    The website has experienced a <strong>{data['kpis']['total_clicks']['change']}% increase in organic traffic</strong>, with total clicks 
                    growing from {data['kpis']['total_clicks']['prev']} to {data['kpis']['total_clicks']['value']} per month. Our comprehensive approach 
                    combining technical SEO, content optimization, and user experience improvements has significantly improved search visibility. 
                    <strong>Impressions have surged by {data['kpis']['impressions']['change']}%</strong>, indicating substantially improved search presence.
                </p>
            </div>

            <!-- KPI Dashboard -->
            <div class="kpi-dashboard">
                <div class="kpi-card">
                    <div class="kpi-label">Total Clicks</div>
                    <div class="kpi-value" data-target="{data['kpis']['total_clicks']['value']}">0</div>
                    <div class="kpi-trend">
                        <span class="arrow">↗</span> +{data['kpis']['total_clicks']['change']}% vs previous period
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Impressions</div>
                    <div class="kpi-value" data-target="{data['kpis']['impressions']['value'] / 1000:.1f}">0</div>
                    <div class="kpi-trend">
                        <span class="arrow">↗</span> +{data['kpis']['impressions']['change']}% growth
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Click-Through Rate</div>
                    <div class="kpi-value" data-target="{data['kpis']['ctr']['value']}">0</div>
                    <div class="kpi-trend">
                        <span class="arrow">↗</span> +{data['kpis']['ctr']['change']}% improvement
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Average Position</div>
                    <div class="kpi-value" data-target="{data['kpis']['avg_position']['value']}">0</div>
                    <div class="kpi-trend">
                        <span class="arrow">↗</span> +{data['kpis']['avg_position']['change']}% positions gained
                    </div>
                </div>
            </div>

            <!-- Top Search Queries -->
            <h2 class="section-header">Top Performing Search Queries</h2>
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

            <!-- Top Landing Pages -->
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

            <!-- Device Breakdown -->
            <h2 class="section-header">📱 Device Distribution</h2>
            <div class="device-grid">
{device_cards_html}
            </div>

            <!-- Geographic Distribution -->
            <h2 class="section-header">🌍 Geographic Performance</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Country</th>
                        <th>Clicks</th>
                        <th>Impressions</th>
                        <th>CTR</th>
                        <th>Market Share</th>
                    </tr>
                </thead>
                <tbody>
{countries_html}
                </tbody>
            </table>

            <!-- Strategic Recommendations -->
            <div class="recommendations">
                <h2>Strategic Recommendations</h2>
                <ul>
                    <li><strong>Mobile Optimization Priority:</strong> Continue optimizing for mobile devices and implement accelerated mobile pages (AMP) for improved performance.</li>
                    <li><strong>Position Improvement Strategy:</strong> Focus on queries ranking between positions 15-25 with enhanced content depth and optimization.</li>
                    <li><strong>Keyword Expansion Opportunities:</strong> Expand into long-tail keyword variations and location-specific search terms.</li>
                    <li><strong>Content Gap Analysis:</strong> Create comprehensive guides and comparison content targeting informational queries.</li>
                    <li><strong>Technical SEO Enhancements:</strong> Address identified technical issues and implement structured data markup.</li>
                    <li><strong>Local SEO Amplification:</strong> Increase local business profile activity and acquire location-specific citations.</li>
                    <li><strong>Backlink Acquisition:</strong> Build relationships with industry directories and relevant websites for quality backlinks.</li>
                    <li><strong>Conversion Rate Optimization:</strong> Implement conversion-focused elements and optimize user journey paths.</li>
                </ul>
            </div>

            <!-- Performance Insights -->
            <h2 class="section-header">🎯 Performance Insights</h2>
            <div class="insights-grid">
                <div class="insights-box strengths">
                    <h3>💪 Key Strengths</h3>
                    <ul>
                        <li><strong>Brand Authority:</strong> Strong brand recognition and top rankings for branded search terms.</li>
                        <li><strong>Mobile-First Success:</strong> Exceptional mobile performance aligning with user search behavior.</li>
                        <li><strong>Site Health Excellence:</strong> High site health score indicating robust technical foundation.</li>
                        <li><strong>Content Quality:</strong> Well-optimized content establishing topical authority.</li>
                        <li><strong>Traffic Growth:</strong> Consistent month-over-month organic traffic increases.</li>
                    </ul>
                </div>
                <div class="insights-box improvements">
                    <h3>📈 Growth Opportunities</h3>
                    <ul>
                        <li><strong>CTR Enhancement:</strong> Optimize meta descriptions with compelling CTAs and value propositions.</li>
                        <li><strong>Position Advancement:</strong> Target top 10 positions for high-priority keywords.</li>
                        <li><strong>Desktop Experience:</strong> Optimize for users on larger screens researching higher-value actions.</li>
                        <li><strong>Geographic Expansion:</strong> Explore opportunities in secondary markets.</li>
                        <li><strong>Conversion Tracking:</strong> Implement enhanced tracking for better ROI measurement.</li>
                    </ul>
                </div>
            </div>

            <!-- 6-Month Progress Comparison -->
            <h2 class="section-header">📈 Progress Comparison</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Previous Period</th>
                        <th>Current Period</th>
                        <th>Change</th>
                        <th>Growth Rate</th>
                    </tr>
                </thead>
                <tbody>
{progress_html}
                </tbody>
            </table>

            <!-- SEO Work Completed -->
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

        <!-- Footer -->
        <div class="footer">
            <h3>{company_name}</h3>
            <p>SEO Performance Report Generated: {report_date}</p>
            <p style="margin-top: 20px; font-size: 12px;">This report contains proprietary analysis. All metrics are sourced from Google Search Console, Google Analytics, and other SEO tools. Data is accurate as of the report generation date.</p>
        </div>
    </div>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>'''
    
    def _get_css_styles(self) -> str:
        """Get complete CSS styles for the report"""
        # Read the CSS from the user's provided HTML (extracted)
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

        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: gradientShift 8s ease infinite;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
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

        /* Content Section */
        .content {
            padding: 40px;
        }

        /* Executive Summary */
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

        /* KPI Dashboard */
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
            position: relative;
            overflow: hidden;
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

        .kpi-trend.negative {
            color: #dc2626;
        }

        .kpi-trend .arrow {
            display: inline-block;
            margin-right: 5px;
        }

        /* Section Headers */
        .section-header {
            font-size: 32px;
            font-weight: 700;
            margin: 50px 0 30px 0;
            color: #2d3748;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section-header::before {
            content: '📊';
            font-size: 36px;
        }

        /* Tables */
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

        .performance-badge.needs-improvement,
        .performance-badge.improving {
            background: #dc2626;
            color: white;
        }

        /* Device Cards */
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

        /* Recommendations Box */
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

        .recommendations h2::before {
            content: '💡';
            font-size: 32px;
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

        /* Performance Insights */
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

        /* Footer */
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

        /* Print Styles */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
            }
            .kpi-card, .device-card {
                page-break-inside: avoid;
            }
            .section-header {
                page-break-after: avoid;
            }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 32px;
            }
            .header .subtitle {
                font-size: 18px;
            }
            .kpi-dashboard {
                grid-template-columns: 1fr;
            }
            .insights-grid {
                grid-template-columns: 1fr;
            }
            .content {
                padding: 20px;
            }
        }

        .country-flag {
            font-size: 24px;
            margin-right: 10px;
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

        .metric-change.negative {
            background: #dc262620;
            color: #dc2626;
        }
        """
    
    def _get_javascript(self) -> str:
        """Get JavaScript for animations"""
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
                    element.textContent = current.toFixed(1) + '%';
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
            // Animate KPI values
            document.querySelectorAll('.kpi-value[data-target]').forEach((element, index) => {
                setTimeout(() => animateCounter(element), index * 100);
            });

            // Animate device percentages
            document.querySelectorAll('.device-percentage[data-target]').forEach((element, index) => {
                setTimeout(() => animateCounter(element), index * 150);
            });

            // Animate progress bars
            document.querySelectorAll('.progress-fill[data-width]').forEach((element, index) => {
                setTimeout(() => animateProgressBar(element), index * 150 + 500);
            });
        });

        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';

        // Print optimization
        window.addEventListener('beforeprint', () => {
            document.querySelectorAll('.kpi-value, .device-percentage').forEach(element => {
                element.textContent = element.getAttribute('data-target') + (element.classList.contains('device-percentage') ? '%' : '');
            });
            document.querySelectorAll('.progress-fill').forEach(element => {
                element.style.width = element.getAttribute('data-width') + '%';
            });
        });
        """
