#!/usr/bin/env python3
"""Test real data integration"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from parsers.csv_parser import CSVParser
from utils.data_normalizer import data_normalizer
from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator

def test_real_data():
    """Test with sample GSC CSV"""

    print("=" * 80)
    print("TESTING REAL DATA INTEGRATION")
    print("=" * 80)

    # Parse GSC CSV
    print("\n📂 Parsing sample GSC CSV...")
    csv_path = "test-data/sample-gsc-hot-tyres.csv"
    parser = CSVParser()
    parsed_data = parser.parse(csv_path)

    if 'error' in parsed_data:
        print(f"❌ Error parsing CSV: {parsed_data['error']}")
        return False

    print(f"✅ Parsed successfully!")
    print(f"   Source: {parsed_data.get('source', 'Unknown')}")
    print(f"   Rows: {len(parsed_data.get('data', []))}")

    # Normalize data
    print("\n🔄 Normalizing data...")
    normalized = data_normalizer.normalize_gsc_data(parsed_data, "Hot Tyres Sydney")

    print(f"✅ Normalized successfully!")
    print(f"   Total Clicks: {normalized['kpis']['total_clicks']['value']}")
    print(f"   Total Impressions: {normalized['kpis']['impressions']['value']}")
    print(f"   Average CTR: {normalized['kpis']['ctr']['value']}%")
    print(f"   Average Position: {normalized['kpis']['avg_position']['value']}")
    print(f"   Top Queries: {len(normalized['top_queries'])}")

    # Generate report with REAL data
    print("\n📊 Generating report with REAL DATA...")
    generator = EnhancedHTMLGenerator()

    html_file = generator.generate_full_report(
        company_name="Hot Tyres Sydney",
        report_period="October 2025",
        seo_data=normalized  # REAL DATA!
    )

    print(f"✅ Report generated: {html_file}")

    # Check file size
    file_path = Path(html_file)
    if file_path.exists():
        size_kb = file_path.stat().st_size / 1024
        print(f"   File size: {size_kb:.1f}KB")
        print(f"   Path: {file_path}")

    print("\n" + "=" * 80)
    print("✅ REAL DATA INTEGRATION TEST PASSED!")
    print("=" * 80)
    print(f"\n🎉 Open the report to see REAL GSC DATA in action:")
    print(f"   file://{file_path.absolute()}")

    return True

if __name__ == "__main__":
    try:
        success = test_real_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
