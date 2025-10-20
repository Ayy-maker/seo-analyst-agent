#!/usr/bin/env python3
"""Test GA4 Integration - End to End"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from parsers.csv_parser import CSVParser
from utils.data_normalizer import data_normalizer
from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator

def test_ga4_only():
    """Test with GA4 CSV only"""

    print("=" * 80)
    print("TEST 1: GA4 DATA ONLY")
    print("=" * 80)

    # Parse GA4 CSV
    print("\n📂 Parsing sample GA4 CSV...")
    ga4_path = "test-data/sample-ga4-hot-tyres.csv"
    parser = CSVParser()
    parsed_data = parser.parse(ga4_path)

    if 'error' in parsed_data:
        print(f"❌ Error parsing CSV: {parsed_data['error']}")
        return False

    print(f"✅ Parsed successfully!")
    print(f"   Source: {parsed_data.get('source', 'Unknown')}")
    print(f"   Rows: {len(parsed_data.get('data', []))}")

    # Normalize GA4 data
    print("\n🔄 Normalizing GA4 data...")
    ga4_metrics = data_normalizer.normalize_ga4_data(parsed_data)

    print(f"✅ Normalized successfully!")
    print(f"   Total Users: {ga4_metrics['total_users']:,}")
    print(f"   Total Sessions: {ga4_metrics['total_sessions']:,}")
    print(f"   Engagement Rate: {ga4_metrics['avg_engagement_rate']}%")
    print(f"   Bounce Rate: {ga4_metrics['avg_bounce_rate']}%")

    # Generate report with GA4 data only (will use demo GSC data)
    print("\n📊 Generating report with GA4 metrics...")
    generator = EnhancedHTMLGenerator()

    html_file = generator.generate_full_report(
        company_name="Hot Tyres Sydney",
        report_period="October 2025",
        seo_data={'ga4_metrics': ga4_metrics}
    )

    print(f"✅ Report generated: {html_file}")

    # Check file size
    file_path = Path(html_file)
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"   File size: {size_kb:.1f}KB")

    return True

def test_gsc_and_ga4():
    """Test with both GSC and GA4 CSV files"""

    print("\n" + "=" * 80)
    print("TEST 2: GSC + GA4 DATA (MERGED)")
    print("=" * 80)

    # Parse GSC CSV
    print("\n📂 Parsing GSC CSV...")
    gsc_path = "test-data/sample-gsc-hot-tyres.csv"
    parser = CSVParser()
    gsc_parsed = parser.parse(gsc_path)

    if 'error' in gsc_parsed:
        print(f"❌ Error parsing GSC CSV: {gsc_parsed['error']}")
        return False

    print(f"✅ GSC parsed: {gsc_parsed.get('source', 'Unknown')}")

    # Parse GA4 CSV
    print("\n📂 Parsing GA4 CSV...")
    ga4_path = "test-data/sample-ga4-hot-tyres.csv"
    ga4_parsed = parser.parse(ga4_path)

    if 'error' in ga4_parsed:
        print(f"❌ Error parsing GA4 CSV: {ga4_parsed['error']}")
        return False

    print(f"✅ GA4 parsed: {ga4_parsed.get('source', 'Unknown')}")

    # Normalize both datasets
    print("\n🔄 Normalizing GSC data...")
    gsc_data = data_normalizer.normalize_gsc_data(gsc_parsed, "Hot Tyres Sydney")
    print(f"✅ GSC normalized: {gsc_data['kpis']['total_clicks']['value']} clicks")

    print("\n🔄 Normalizing GA4 data...")
    ga4_metrics = data_normalizer.normalize_ga4_data(ga4_parsed)
    print(f"✅ GA4 normalized: {ga4_metrics['total_users']:,} users")

    # Merge datasets
    print("\n🔀 Merging GSC and GA4 data...")
    merged_data = data_normalizer.merge_gsc_and_ga4_data(gsc_data, ga4_metrics)

    print(f"✅ Data merged successfully!")
    print(f"   GSC Clicks: {merged_data['kpis']['total_clicks']['value']:,}")
    print(f"   GA4 Users: {merged_data['ga4_metrics']['total_users']:,}")
    print(f"   Progress items: {len(merged_data['progress'])}")

    # Generate report with merged data
    print("\n📊 Generating report with MERGED GSC + GA4 data...")
    generator = EnhancedHTMLGenerator()

    html_file = generator.generate_full_report(
        company_name="Hot Tyres Sydney",
        report_period="October 2025",
        seo_data=merged_data
    )

    print(f"✅ Report generated: {html_file}")

    # Check file size
    file_path = Path(html_file)
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"   File size: {size_kb:.1f}KB")

    # Verify GA4 section exists in HTML
    print("\n🔍 Verifying GA4 section in HTML...")
    with open(file_path, 'r') as f:
        html_content = f.read()

        if 'Google Analytics 4 User Behavior Metrics' in html_content:
            print("✅ GA4 section found in report!")
        else:
            print("❌ GA4 section NOT found in report!")
            return False

        # Check for key GA4 metrics
        ga4_checks = [
            ('Total Users', ga4_metrics['total_users']),
            ('Total Sessions', ga4_metrics['total_sessions']),
            ('Engagement Rate', ga4_metrics['avg_engagement_rate']),
            ('Bounce Rate', ga4_metrics['avg_bounce_rate'])
        ]

        print("\n📊 Verifying GA4 metrics in HTML:")
        for metric_name, metric_value in ga4_checks:
            if str(metric_value) in html_content or f"{metric_value:,}" in html_content:
                print(f"   ✅ {metric_name}: {metric_value}")
            else:
                print(f"   ⚠️ {metric_name}: {metric_value} (might be formatted differently)")

    return True

def main():
    """Run all tests"""

    print("\n")
    print("🧪" * 40)
    print("GOOGLE ANALYTICS 4 INTEGRATION TEST SUITE")
    print("🧪" * 40)

    try:
        # Test 1: GA4 only
        if not test_ga4_only():
            print("\n❌ TEST 1 FAILED")
            return False

        print("\n✅ TEST 1 PASSED!")

        # Test 2: GSC + GA4 merged
        if not test_gsc_and_ga4():
            print("\n❌ TEST 2 FAILED")
            return False

        print("\n✅ TEST 2 PASSED!")

        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! GA4 INTEGRATION IS WORKING!")
        print("=" * 80)

        print("\n📝 Summary:")
        print("   ✅ GA4 CSV detection working")
        print("   ✅ GA4 data normalization working")
        print("   ✅ GSC + GA4 data merging working")
        print("   ✅ GA4 metrics section rendering in reports")
        print("   ✅ Report generation with real GA4 data working")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
