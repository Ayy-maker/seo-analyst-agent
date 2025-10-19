#!/usr/bin/env python3
"""
Generate Sample Enhanced PDF Report
Demonstrates all Phase 4 features with realistic data
"""

from datetime import datetime, date, timedelta
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

from agents.reporter.enhanced_pdf_generator import EnhancedPDFReportGenerator
from database import DatabaseManager
import random

def generate_sample_data():
    """Generate realistic sample insights"""
    
    insights = [
        # Keywords Module
        {
            'module': 'keywords',
            'type': 'opportunity',
            'severity': 'high',
            'insight': 'Top keyword "best seo tools" dropped 5 positions from #3 to #8. Immediate content refresh recommended.',
            'metric_value': -5
        },
        {
            'module': 'keywords',
            'type': 'win',
            'severity': 'low',
            'insight': 'Strong performance: 12 keywords improved rankings this month, average gain of +3.2 positions.',
            'metric_value': 12
        },
        {
            'module': 'keywords',
            'type': 'issue',
            'severity': 'medium',
            'insight': 'Keyword cannibalization detected: "seo analysis" ranks on 3 different URLs. Consolidation recommended.',
            'metric_value': 3
        },
        {
            'module': 'keywords',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': '5 keywords in positions 11-15 (page 2) with high search volume. Small optimization could push to page 1.',
            'metric_value': 5
        },
        
        # Technical SEO Module
        {
            'module': 'technical',
            'type': 'issue',
            'severity': 'high',
            'insight': 'Core Web Vitals: LCP exceeds 4 seconds on 15 pages. Server response time optimization needed.',
            'metric_value': 15
        },
        {
            'module': 'technical',
            'type': 'issue',
            'severity': 'high',
            'insight': '23 pages returning 404 errors. These broken pages are losing potential traffic and authority.',
            'metric_value': 23
        },
        {
            'module': 'technical',
            'type': 'win',
            'severity': 'low',
            'insight': 'Mobile usability score improved to 95/100. All mobile-friendly issues resolved.',
            'metric_value': 95
        },
        {
            'module': 'technical',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': 'XML sitemap contains 142 URLs, but only 87 are indexed. Investigate indexation blockers.',
            'metric_value': 55
        },
        
        # On-Page SEO Module
        {
            'module': 'onpage',
            'type': 'issue',
            'severity': 'medium',
            'insight': '34 pages have duplicate meta descriptions. Each page needs unique, compelling descriptions.',
            'metric_value': 34
        },
        {
            'module': 'onpage',
            'type': 'opportunity',
            'severity': 'low',
            'insight': '18 images missing alt text. Adding descriptive alt attributes improves accessibility and SEO.',
            'metric_value': 18
        },
        {
            'module': 'onpage',
            'type': 'win',
            'severity': 'low',
            'insight': 'Content quality score increased to 82/100. Recent blog posts are well-optimized and engaging.',
            'metric_value': 82
        },
        {
            'module': 'onpage',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': 'Schema markup implemented on only 40% of pages. Expanding structured data could improve SERP features.',
            'metric_value': 40
        },
        
        # Backlinks Module
        {
            'module': 'backlinks',
            'type': 'win',
            'severity': 'low',
            'insight': 'Gained 47 new high-quality backlinks this month. Domain authority increased by 2 points to DA 58.',
            'metric_value': 47
        },
        {
            'module': 'backlinks',
            'type': 'issue',
            'severity': 'high',
            'insight': '12 toxic backlinks detected from spammy domains. Disavow file should be updated immediately.',
            'metric_value': 12
        },
        {
            'module': 'backlinks',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': 'Lost 8 backlinks from authority sites. Outreach campaign recommended to reclaim these links.',
            'metric_value': 8
        },
        
        # Traffic Module
        {
            'module': 'traffic',
            'type': 'win',
            'severity': 'low',
            'insight': 'Organic traffic increased 26.9% to 1,524 sessions. Strong growth driven by improved rankings.',
            'metric_value': 26.9
        },
        {
            'module': 'traffic',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': 'Bounce rate on blog posts is 68%. Internal linking and content engagement strategies needed.',
            'metric_value': 68
        },
        {
            'module': 'traffic',
            'type': 'win',
            'severity': 'low',
            'insight': 'Mobile traffic now represents 62% of total sessions. Mobile-first optimization paying off.',
            'metric_value': 62
        },
        {
            'module': 'traffic',
            'type': 'opportunity',
            'severity': 'low',
            'insight': 'Average session duration is 2:15. Improving content depth could increase engagement.',
            'metric_value': 135
        }
    ]
    
    return insights

def populate_sample_historical_data(db: DatabaseManager, client_id: int):
    """Populate database with historical data for demo"""
    
    print("\n📊 Populating historical data...")
    
    # Generate 6 months of historical traffic data
    today = date.today()
    for days_ago in range(180, 0, -1):
        report_date = today - timedelta(days=days_ago)
        
        # Create traffic data with growth trend
        base_sessions = 1000
        growth_factor = (180 - days_ago) / 180  # Gradual growth
        noise = random.randint(-50, 50)
        sessions = int(base_sessions + (growth_factor * 400) + noise)
        
        traffic_data = [{
            'date': report_date,
            'sessions': sessions,
            'users': int(sessions * 0.85),
            'pageviews': int(sessions * 2.3),
            'bounce_rate': random.uniform(60, 75),
            'avg_session_duration': random.uniform(120, 180),
            'source': 'organic',
            'device': 'desktop'
        }]
        
        # Create a dummy report entry
        report_id = db.create_report(
            client_id=client_id,
            report_date=report_date,
            report_period=f"Day {180-days_ago}",
            insights_count=random.randint(15, 25),
            health_score=random.randint(70, 85)
        )
        
        # Store traffic
        db.save_traffic(report_id, client_id, traffic_data)
        
        # Store some sample metrics
        metrics = [
            {
                'name': 'organic_traffic',
                'value': sessions,
                'unit': 'sessions',
                'date': report_date,
                'module': 'traffic'
            },
            {
                'name': 'avg_position',
                'value': random.uniform(8, 12),
                'unit': 'position',
                'date': report_date,
                'module': 'keywords'
            }
        ]
        db.save_metrics(report_id, client_id, metrics)
    
    # Add some keywords with position history
    keywords = [
        'best seo tools',
        'seo analysis',
        'keyword research',
        'seo software',
        'seo platform'
    ]
    
    for days_ago in range(30, 0, -1):
        report_date = today - timedelta(days=days_ago)
        report_id = db.get_reports(client_id, limit=1)[0]['id']
        
        keyword_data = []
        for keyword in keywords:
            # Simulate position changes
            base_position = random.randint(5, 15)
            position = max(1, base_position + random.randint(-2, 2))
            
            keyword_data.append({
                'keyword': keyword,
                'position': position,
                'previous_position': position + random.randint(-1, 1),
                'position_change': random.uniform(-2, 2),
                'impressions': random.randint(500, 2000),
                'clicks': random.randint(50, 300),
                'ctr': random.uniform(3.0, 8.0),
                'date': report_date
            })
        
        db.save_keywords(report_id, client_id, keyword_data)
    
    print("✅ Historical data populated (180 days)")

def main():
    """Generate sample enhanced report"""
    
    print("="*60)
    print("🎨 GENERATING SAMPLE ENHANCED PDF REPORT")
    print("="*60)
    
    # Initialize
    print("\n🔧 Initializing system...")
    db = DatabaseManager()
    generator = EnhancedPDFReportGenerator(use_database=True)
    
    # Get or create demo client
    print("👤 Setting up demo client...")
    client_name = "Demo Corporation"
    client = db.get_client(name=client_name)
    
    if not client:
        client_id = db.create_client(
            name=client_name,
            domain="demo-corp.com",
            industry="Technology"
        )
        print(f"✓ Created demo client: {client_name}")
        
        # Populate historical data for demo
        populate_sample_historical_data(db, client_id)
    else:
        client_id = client['id']
        print(f"✓ Using existing demo client: {client_name}")
    
    # Generate sample insights
    print("\n📝 Generating sample insights...")
    insights = generate_sample_data()
    print(f"✓ Generated {len(insights)} realistic insights")
    
    # Store current report
    print("\n💾 Storing report in database...")
    report_id = db.create_report(
        client_id=client_id,
        report_date=date.today(),
        report_period="Monthly Analysis - Sample Report",
        insights_count=len(insights),
        health_score=76
    )
    db.save_insights(report_id, client_id, insights)
    print(f"✓ Report #{report_id} stored")
    
    # Generate enhanced PDF
    print("\n🎨 Generating ENHANCED PDF with Phase 4 features...")
    print("   This includes:")
    print("   • Historical comparisons")
    print("   • Growth timeline chart")
    print("   • Month-over-month analysis")
    print("   • Anomaly alerts")
    print("   • Traffic forecasts")
    print("   • Key wins section")
    print("   • And much more...")
    
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    pdf_file = generator.generate_full_report(
        insights=insights,
        company_name=client_name,
        report_period="Sample Monthly Report - October 2024",
        client_id=client_id,
        filename=f"SAMPLE-enhanced-report-{timestamp}.pdf"
    )
    
    print("\n" + "="*60)
    print("✨ SAMPLE REPORT GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📄 Report Location: {pdf_file}")
    print(f"📊 Client: {client_name}")
    print(f"🔢 Insights: {len(insights)}")
    print(f"🎯 Health Score: 76/100")
    print(f"📈 Historical Data: 180 days")
    
    print("\n🎁 WHAT'S INSIDE:")
    print("   ✅ Table of Contents")
    print("   ✅ Executive Summary with Growth Context")
    print("   ✅ KPI Dashboard with Historical Comparison")
    print("   ✅ Health Score with 3-Month Trend")
    print("   ✅ Growth Timeline (6-month chart)")
    print("   ✅ Month-over-Month Comparison Table")
    print("   ✅ Anomaly Alerts Section")
    print("   ✅ Top Findings with Visual Badges")
    print("   ✅ 5 Module Deep-Dive Reports")
    print("   ✅ Traffic Forecast (90-day prediction)")
    print("   ✅ Key Wins & Improvements")
    print("   ✅ Prioritized Recommendations")
    print("   ✅ Strategic Performance Insights")
    
    print("\n💡 TO VIEW:")
    print(f"   open {pdf_file}")
    
    print("\n🎨 VISUAL FEATURES:")
    print("   • Professional gradient headers")
    print("   • Beautiful time-series charts")
    print("   • Color-coded severity badges (🔴 🟡 🟢)")
    print("   • Growth indicators (↗️ ↘️)")
    print("   • Confidence interval bands")
    print("   • Frosted glass effects")
    print("   • Shadow depth layers")
    print("   • 200 DPI print quality")
    
    print("\n" + "="*60)
    print("🎉 Ready to impress your clients!")
    print("="*60 + "\n")
    
    return pdf_file

if __name__ == '__main__':
    pdf_path = main()
