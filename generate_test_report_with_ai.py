#!/usr/bin/env python3
"""
Generate test report with AI insights enabled
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient
from utils.data_normalizer import data_normalizer
from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("\n" + "="*70)
    print("🤖 GENERATING TEST REPORT WITH AI INSIGHTS")
    print("="*70)

    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Error: Anthropic API key not configured")
        return False

    print(f"\n✅ API Key configured: {api_key[:15]}...{api_key[-4:]}")

    # Configuration
    company_name = "The Profit Platform"
    ga4_property_id = "500340846"
    gsc_property = "sc-domain:theprofitplatform.com.au"

    print(f"\n📋 Generating report for: {company_name}")
    print(f"   GA4 Property: {ga4_property_id}")
    print(f"   GSC Property: {gsc_property}")

    # Fetch GSC data
    print("\n1️⃣  Fetching Google Search Console data...")
    try:
        gsc_client = GSCAPIClient()
        if not gsc_client.connect():
            print("❌ GSC connection failed")
            return False

        queries = gsc_client.fetch_queries_with_metrics(gsc_property, days=30)
        if not queries:
            print("❌ No GSC data available")
            return False

        print(f"   ✅ Fetched {len(queries)} search queries")

        # Normalize GSC data
        gsc_parsed = {
            'source': 'Google Search Console',
            'site_url': gsc_property,
            'record_count': len(queries),
            'data': queries
        }
        normalized_data = data_normalizer.normalize_gsc_data(gsc_parsed, company_name)

    except Exception as e:
        print(f"❌ GSC Error: {e}")
        return False

    # Fetch GA4 data
    print("\n2️⃣  Fetching Google Analytics 4 data...")
    try:
        ga4_client = GA4APIClient(property_id=ga4_property_id)
        if not ga4_client.connect():
            print("❌ GA4 connection failed")
            return False

        behavior_data = ga4_client.fetch_user_behavior(days=30)
        if 'error' in behavior_data:
            print(f"❌ GA4 Error: {behavior_data['error']}")
            return False

        print(f"   ✅ Fetched {behavior_data.get('total_rows', 0)} days of data")

        # Normalize GA4 data
        ga4_parsed = {
            'source': 'Google Analytics 4',
            'property_id': ga4_property_id,
            'record_count': behavior_data.get('total_rows', 0),
            'data': behavior_data.get('data', [])
        }
        ga4_metrics = data_normalizer.normalize_ga4_data(ga4_parsed)

    except Exception as e:
        print(f"❌ GA4 Error: {e}")
        return False

    # Merge data
    print("\n3️⃣  Merging GSC and GA4 data...")
    merged_data = data_normalizer.merge_gsc_and_ga4_data(normalized_data, ga4_metrics)
    print("   ✅ Data merged successfully")

    # Generate AI insights
    print("\n4️⃣  Generating AI-powered insights...")
    print("   (This may take 10-15 seconds for AI analysis...)")

    try:
        from agents.analyst import AnalystAgent
        from utils.prioritization_engine import prioritization_engine

        analyst = AnalystAgent(api_key, "config")

        # Generate comprehensive AI analysis
        print("   📊 Analyzing SEO performance with Claude Sonnet 4.5...")
        recommendations = analyst.generate_strategic_recommendations(merged_data, company_name)
        print(f"   ✅ Generated {len(recommendations)} AI recommendations")

        # Prioritize recommendations
        print("   🎯 Prioritizing recommendations...")
        prioritized_recs = prioritization_engine.prioritize_recommendations(recommendations)
        priority_summary = prioritization_engine.get_priority_summary(prioritized_recs)

        print(f"   ✅ Prioritization complete:")
        print(f"      ⚡ Quick Wins: {priority_summary['breakdown']['quick_wins']}")
        print(f"      🎯 High Impact: {priority_summary['breakdown']['high_impact']}")
        print(f"      📊 Strategic: {priority_summary['breakdown']['strategic']}")

        # Add AI insights to merged_data
        if 'phase3' not in merged_data:
            merged_data['phase3'] = {}

        merged_data['phase3']['prioritized_recommendations'] = prioritized_recs
        merged_data['phase3']['priority_summary'] = priority_summary

    except Exception as e:
        print(f"   ⚠️  AI generation failed: {e}")
        print("   Continuing with report generation without AI insights...")
        import traceback
        traceback.print_exc()

    # Generate report with AI
    print("\n5️⃣  Generating HTML report...")
    print("   (Embedding AI insights into report...)")

    try:
        html_generator = EnhancedHTMLGenerator()
        html_file = html_generator.generate_full_report(
            company_name=company_name,
            report_period=datetime.now().strftime('%B %Y'),
            seo_data=merged_data
        )

        print(f"\n✅ Report generated successfully!")
        print(f"   📄 File: {html_file}")

        # Check file size (AI reports are typically larger)
        file_size = Path(html_file).stat().st_size
        print(f"   📊 Size: {file_size:,} bytes")

        # Read report and check for AI content
        with open(html_file, 'r') as f:
            content = f.read()

        print("\n6️⃣  Verifying AI content...")

        # Check for indicators of AI-generated content
        has_quick_wins = '⚡' in content and 'Quick Win' in content
        has_high_impact = '🎯' in content and 'High Impact' in content
        has_strategic = '📊' in content and 'Strategic' in content
        has_no_recommendations = 'No recommendations available' in content or '0 Quick Wins' in content

        print(f"\n   Results:")
        print(f"   {'✅' if has_quick_wins else '❌'} Quick Wins present")
        print(f"   {'✅' if has_high_impact else '❌'} High Impact items present")
        print(f"   {'✅' if has_strategic else '❌'} Strategic items present")
        print(f"   {'✅' if not has_no_recommendations else '❌'} Has recommendations (not empty)")

        if has_quick_wins and has_high_impact and not has_no_recommendations:
            print("\n🎉 SUCCESS: AI insights are working!")
            print(f"\n📖 View report at:")
            print(f"   https://seo.theprofitplatform.com.au/preview/{html_file}")
        else:
            print("\n⚠️  WARNING: AI insights may not be generating")
            print("   Check web/app.py to ensure AI agents are being called")

        return True

    except Exception as e:
        print(f"\n❌ Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
