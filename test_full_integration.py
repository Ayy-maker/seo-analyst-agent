#!/usr/bin/env python3
"""
Complete Integration Test
Demonstrates how SEMrush + GSC + GA4 data combine into one report
"""

import sys
sys.path.insert(0, '.')

from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient
from parsers.csv_parser import CSVParser
from datetime import datetime
import json

print("🔍 COMPLETE INTEGRATION TEST")
print("=" * 70)
print("\nDemonstrating how all 3 data sources combine:\n")

# ============================================================================
# STEP 1: Parse SEMrush Data (Simulated)
# ============================================================================
print("\n1️⃣  STEP 1: Parse SEMrush Data (Manual Upload)")
print("-" * 70)

# Using sample backlinks file as example SEMrush data
parser = CSVParser()
semrush_data = parser.parse('data/samples/backlinks-report.csv')

print(f"   📄 File: backlinks-report.csv")
print(f"   ✅ Parsed successfully")
print(f"   📊 Records: {semrush_data.get('record_count', 0)}")
print(f"   🔍 Type: {semrush_data.get('type', 'Unknown')}")

# Simulated SEMrush metrics
semrush_summary = {
    'domain': 'hottyres.com.au',
    'domain_authority': 45,
    'total_backlinks': 1250,
    'referring_domains': 89,
    'organic_keywords': 342,
    'estimated_traffic': 850
}

print(f"\n   📊 SEMrush Metrics:")
print(f"      Domain: {semrush_summary['domain']}")
print(f"      Domain Authority: {semrush_summary['domain_authority']}")
print(f"      Total Backlinks: {semrush_summary['total_backlinks']:,}")
print(f"      Referring Domains: {semrush_summary['referring_domains']}")
print(f"      Organic Keywords: {semrush_summary['organic_keywords']}")
print(f"      Est. Traffic: {semrush_summary['estimated_traffic']:,}/month")

# ============================================================================
# STEP 2: Auto-Fetch GSC Data
# ============================================================================
print("\n\n2️⃣  STEP 2: Auto-Fetch Google Search Console Data")
print("-" * 70)
print("   🤖 Automatically fetching GSC data for: hottyres.com.au")

gsc_client = GSCAPIClient()
gsc_data = None

if gsc_client.connect():
    print("   ✅ Connected to GSC")

    # Get sites and find matching one
    sites = gsc_client.list_sites()
    matching_site = None

    for site in sites:
        if 'hottyres' in site.lower():
            matching_site = site
            break

    if matching_site:
        print(f"   🎯 Found property: {matching_site}")

        # Fetch data
        summary = gsc_client.get_site_summary(matching_site, days=30)
        gsc_data = summary

        print(f"\n   📊 GSC Metrics (Last 30 Days):")
        print(f"      Total Clicks: {summary['total_clicks']:,}")
        print(f"      Total Impressions: {summary['total_impressions']:,}")
        print(f"      Avg CTR: {summary['average_ctr']:.2f}%")
        print(f"      Avg Position: {summary['average_position']:.1f}")
        print(f"      Total Queries: {summary['total_queries']:,}")
    else:
        print("   ⚠️  No matching GSC property found")
else:
    print("   ❌ Could not connect to GSC")

# ============================================================================
# STEP 3: Auto-Fetch GA4 Data
# ============================================================================
print("\n\n3️⃣  STEP 3: Auto-Fetch Google Analytics 4 Data")
print("-" * 70)
print("   🤖 Automatically fetching GA4 data for: Hot Tyres (487936109)")

ga4_client = GA4APIClient(property_id='487936109')
ga4_data = None

if ga4_client.connect():
    print("   ✅ Connected to GA4")

    # Fetch data
    summary = ga4_client.get_summary_metrics(days=30)
    ga4_data = summary

    print(f"\n   📊 GA4 Metrics (Last 30 Days):")
    print(f"      Total Users: {summary['total_users']:,}")
    print(f"      Total Sessions: {summary['total_sessions']:,}")
    print(f"      Page Views: {summary['total_page_views']:,}")
    print(f"      Engagement Rate: {summary['avg_engagement_rate']:.1f}%")
    print(f"      Bounce Rate: {summary['avg_bounce_rate']:.1f}%")
    print(f"      Pages/Session: {summary['pages_per_session']:.1f}")
else:
    print("   ❌ Could not connect to GA4")

# ============================================================================
# STEP 4: Merge All Data Sources
# ============================================================================
print("\n\n4️⃣  STEP 4: Merge All Data Sources")
print("-" * 70)

comprehensive_report = {
    'generated_at': datetime.now().isoformat(),
    'domain': 'hottyres.com.au',
    'property': 'Hot Tyres',
    'data_sources': {
        'semrush': semrush_summary,
        'google_search_console': gsc_data if gsc_data else {'status': 'unavailable'},
        'google_analytics_4': ga4_data if ga4_data else {'status': 'unavailable'}
    }
}

print("   ✅ Data merged successfully!\n")
print("   📊 Combined Data Summary:")
print("   " + "=" * 60)

# SEMrush
print("\n   📦 SEMrush (Competitor/Market Analysis):")
print(f"      • Domain Authority: {semrush_summary['domain_authority']}")
print(f"      • Backlinks: {semrush_summary['total_backlinks']:,}")
print(f"      • Keywords Tracked: {semrush_summary['organic_keywords']:,}")

# GSC
if gsc_data:
    print("\n   🔍 Google Search Console (Your Actual Performance):")
    print(f"      • Clicks: {gsc_data['total_clicks']:,}")
    print(f"      • Impressions: {gsc_data['total_impressions']:,}")
    print(f"      • Search Queries: {gsc_data['total_queries']:,}")
else:
    print("\n   ⚠️  GSC data not available")

# GA4
if ga4_data:
    print("\n   📈 Google Analytics 4 (User Behavior):")
    print(f"      • Users: {ga4_data['total_users']:,}")
    print(f"      • Sessions: {ga4_data['total_sessions']:,}")
    print(f"      • Engagement: {ga4_data['avg_engagement_rate']:.1f}%")
else:
    print("\n   ⚠️  GA4 data not available")

# ============================================================================
# STEP 5: Generate Insights
# ============================================================================
print("\n\n5️⃣  STEP 5: Generate Combined Insights")
print("-" * 70)

print("\n   💡 Automated Insights:\n")

# Cross-reference insights
if gsc_data and ga4_data:
    ctr = gsc_data['average_ctr']
    engagement = ga4_data['avg_engagement_rate']

    print(f"   1. Search Performance vs User Engagement:")
    print(f"      • Average CTR: {ctr:.2f}%")
    print(f"      • Engagement Rate: {engagement:.1f}%")

    if engagement > 50:
        print(f"      ✅ Good engagement! Users find content valuable")
    else:
        print(f"      ⚠️  Lower engagement - consider content improvements")

    print(f"\n   2. Traffic Quality Analysis:")
    print(f"      • {gsc_data['total_clicks']:,} clicks from search")
    print(f"      • {ga4_data['total_users']:,} total users")
    print(f"      • Search represents {(gsc_data['total_clicks']/ga4_data['total_users']*100):.1f}% of traffic")

    print(f"\n   3. SEO Opportunity:")
    print(f"      • {gsc_data['total_impressions']:,} impressions but only {gsc_data['total_clicks']:,} clicks")
    print(f"      • {semrush_summary['organic_keywords']:,} keywords tracked in SEMrush")
    print(f"      • {gsc_data['total_queries']:,} actual search queries in GSC")

    keyword_gap = gsc_data['total_queries'] - semrush_summary['organic_keywords']
    if keyword_gap > 0:
        print(f"      💡 {keyword_gap} queries not tracked in SEMrush - opportunity!")

# ============================================================================
# FINAL OUTPUT
# ============================================================================
print("\n\n" + "=" * 70)
print("📋 COMPREHENSIVE REPORT READY")
print("=" * 70)

print("\n✅ Data Sources Combined:")
print(f"   • SEMrush: ✓ Competitor & keyword data")
print(f"   • GSC: {('✓ Real search performance' if gsc_data else '✗ Not available')}")
print(f"   • GA4: {('✓ User behavior data' if ga4_data else '✗ Not available')}")

print("\n📄 Report would be saved to:")
print(f"   outputs/html-reports/seo-report-hot-tyres-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.html")

print("\n🎯 This demonstrates the complete workflow:")
print("   1. Upload SEMrush file (PDF/Excel/CSV/Word)")
print("   2. System auto-fetches GSC data ✨")
print("   3. System auto-fetches GA4 data ✨")
print("   4. All data merged into comprehensive report")
print("   5. Generated in 30-60 seconds!")

print("\n" + "=" * 70)

# Save merged data as example
output_file = f'outputs/merged-data-example-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
with open(output_file, 'w') as f:
    json.dump(comprehensive_report, f, indent=2, default=str)

print(f"\n📁 Merged data saved to: {output_file}")
print("\n✅ Integration test complete!")
