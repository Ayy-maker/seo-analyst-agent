#!/usr/bin/env python3
"""
Generate Enhanced Sample Report
Creates stunning HTML report with charts and animations
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator
from datetime import datetime

def generate_enhanced_sample():
    """Generate enhanced sample report with realistic SEO data"""
    
    # Sample data with month-over-month growth
    seo_data = {
        'kpis': {
            'total_clicks': {'value': 258, 'change': 286, 'prev': 67},
            'impressions': {'value': 8700, 'change': 412, 'prev': 1698},
            'ctr': {'value': 2.97, 'change': 25, 'prev': 2.4},
            'avg_position': {'value': 18.4, 'change': 40, 'prev': 30.7}
        },
        'top_queries': [
            {'rank': 1, 'query': 'branded company term', 'clicks': 89, 'impressions': 1247, 'ctr': 7.1, 'position': 2.3, 'performance': 'Excellent'},
            {'rank': 2, 'query': 'industry keyword phrase', 'clicks': 42, 'impressions': 1834, 'ctr': 2.3, 'position': 12.7, 'performance': 'Good'},
            {'rank': 3, 'query': 'service related search', 'clicks': 38, 'impressions': 2156, 'ctr': 1.8, 'position': 15.2, 'performance': 'Good'},
            {'rank': 4, 'query': 'product category term', 'clicks': 27, 'impressions': 1423, 'ctr': 1.9, 'position': 18.5, 'performance': 'Good'},
            {'rank': 5, 'query': 'solution based query', 'clicks': 19, 'impressions': 987, 'ctr': 1.9, 'position': 21.3, 'performance': 'Improving'},
            {'rank': 6, 'query': 'location service keyword', 'clicks': 15, 'impressions': 1245, 'ctr': 1.2, 'position': 24.8, 'performance': 'Improving'},
            {'rank': 7, 'query': 'specialty niche term', 'clicks': 12, 'impressions': 654, 'ctr': 1.8, 'position': 19.4, 'performance': 'Good'},
            {'rank': 8, 'query': 'specific product name', 'clicks': 9, 'impressions': 543, 'ctr': 1.7, 'position': 22.1, 'performance': 'Improving'},
        ],
        'landing_pages': [
            {'url': '/', 'label': 'Homepage', 'clicks': 134, 'change': 298, 'impressions': 4523, 'ctr': 3.0, 'position': 8.2},
            {'url': '/services/', 'label': 'Services Page', 'clicks': 47, 'change': 385, 'impressions': 2167, 'ctr': 2.2, 'position': 16.4},
            {'url': '/products/', 'label': 'Products Overview', 'clicks': 28, 'change': 450, 'impressions': 1234, 'ctr': 2.3, 'position': 18.7},
            {'url': '/about/', 'label': 'About Us', 'clicks': 22, 'change': 420, 'impressions': 987, 'ctr': 2.2, 'position': 21.5},
            {'url': '/contact/', 'label': 'Contact Page', 'clicks': 17, 'change': 325, 'impressions': 656, 'ctr': 2.6, 'position': 14.3},
        ],
        'devices': [
            {'device': 'Mobile', 'icon': '📱', 'clicks': 175, 'percentage': 67.8},
            {'device': 'Desktop', 'icon': '💻', 'clicks': 74, 'percentage': 28.7},
            {'device': 'Tablet', 'icon': '📟', 'clicks': 9, 'percentage': 3.5},
        ],
        'monthly_progress': [
            {'month': 'March 2025', 'clicks': 67, 'impressions': 1698, 'ctr': 2.4, 'position': 30.7, 'health': 72},
            {'month': 'April 2025', 'clicks': 89, 'impressions': 2854, 'ctr': 2.5, 'position': 28.3, 'health': 75},
            {'month': 'May 2025', 'clicks': 124, 'impressions': 4123, 'ctr': 2.6, 'position': 25.1, 'health': 78},
            {'month': 'June 2025', 'clicks': 167, 'impressions': 5892, 'ctr': 2.7, 'position': 22.4, 'health': 82},
            {'month': 'July 2025', 'clicks': 208, 'impressions': 7234, 'ctr': 2.8, 'position': 20.1, 'health': 85},
            {'month': 'August 2025', 'clicks': 232, 'impressions': 7989, 'ctr': 2.9, 'position': 19.2, 'health': 86},
            {'month': 'September 2025', 'clicks': 258, 'impressions': 8701, 'ctr': 3.0, 'position': 18.4, 'health': 87},
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
    
    print("="*70)
    print("🎨 GENERATING ENHANCED SAMPLE REPORT")
    print("="*70)
    
    # Generate HTML report
    print("\n📊 Generating enhanced HTML report with interactive charts...")
    html_generator = EnhancedHTMLGenerator()
    html_file = html_generator.generate_full_report(
        company_name="Sample Company",
        report_period="6-Month Progress Report | March - September 2025",
        seo_data=seo_data,
        filename="SAMPLE-enhanced-report.html"
    )
    
    print(f"✅ HTML report generated: {html_file}")
    print(f"   Size: {Path(html_file).stat().st_size // 1024}KB")
    
    print("\n" + "="*70)
    print("✨ ENHANCED REPORT READY!")
    print("="*70)
    print(f"\n📄 Location: {html_file}")
    print("\n🎁 WHAT'S INSIDE:")
    print("   ✅ Executive Summary with Growth Context")
    print("   ✅ Animated KPI Dashboard (4 key metrics)")
    print("   ✅ Interactive Chart.js Visualizations:")
    print("      • Clicks Trend (line chart)")
    print("      • Health Score Progress (bar chart)")
    print("      • Impressions Growth (line chart)")
    print("      • Position Improvement (inverted line chart)")
    print("   ✅ Top Performing Search Queries (5 keywords)")
    print("   ✅ Top Landing Pages with Growth Indicators")
    print("   ✅ Device Distribution with Animated Progress Bars")
    print("   ✅ 6-Month Comparison Table (8 metrics)")
    print("   ✅ Strategic Recommendations (8 actionable items)")
    print("   ✅ Performance Insights (Strengths & Opportunities)")
    print("   ✅ SEO Deliverables Completed (10 items)")
    print("\n💡 TO VIEW:")
    print(f"   open {html_file}")
    
    print("\n🎨 ENHANCED FEATURES:")
    print("   • 4 Interactive Chart.js visualizations")
    print("   • Beautiful gradient animations")
    print("   • Interactive hover effects on all elements")
    print("   • Smooth counter animations")
    print("   • Animated progress bars")
    print("   • Fully responsive design (mobile-ready)")
    print("   • Print-optimized layout")
    print("   • Month-over-month growth tracking (7 months)")
    print("   • Color-coded performance badges")
    print("   • Professional Inter font typography")
    print("   • Box shadows and depth effects")
    print("   • Glassmorphism date badge")
    
    print("\n🚀 IMPROVEMENTS OVER PREVIOUS VERSION:")
    print("   • Added interactive Chart.js graphs (NEW!)")
    print("   • Removed geographic section (as requested)")
    print("   • Enhanced progress comparison (2 more metrics)")
    print("   • Month-over-month visualization")
    print("   • Better animations and transitions")
    print("   • Improved color scheme and gradients")
    print("   • More detailed insights sections")
    print("   • Professional single-page layout")
    
    print("\n" + "="*70)
    print("🎉 10X BETTER - READY FOR PRODUCTION!")
    print("="*70 + "\n")
    
    return html_file

if __name__ == '__main__':
    html_path = generate_enhanced_sample()
