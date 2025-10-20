#!/usr/bin/env python3
"""
Generate test report with Phase 1 improvements
Tests the complete pipeline from company name to HTML report
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator


def generate_test_reports():
    """Generate test reports for various industries"""
    generator = EnhancedHTMLGenerator()

    test_companies = [
        "Hot Tyres Sydney",
        "Smith Law Firm Melbourne",
        "Bright Smile Dental Clinic Perth"
    ]

    output_dir = Path(__file__).parent / "outputs" / "test-reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("GENERATING TEST REPORTS WITH PHASE 1 IMPROVEMENTS")
    print("=" * 80)

    for company_name in test_companies:
        print(f"\n📊 Generating report for: {company_name}")

        # Generate report period string
        report_period = f"March - September {datetime.now().year}"

        # Generate the report HTML
        report_html = generator.generate_full_report(
            company_name=company_name,
            report_period=report_period
        )

        # Save to file
        safe_filename = company_name.lower().replace(" ", "-").replace("&", "and")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = output_dir / f"seo-report-{safe_filename}-{timestamp}.html"

        output_file.write_text(report_html)

        print(f"   ✅ Report saved to: {output_file}")

        # Quick verification - check if it contains realistic keywords
        if "sample keyword" in report_html.lower():
            print(f"   ❌ WARNING: Report still contains 'sample keyword' placeholders!")
        else:
            print(f"   ✅ No 'sample keyword' placeholders found")

        # Check for industry-specific content
        if company_name == "Hot Tyres Sydney":
            if "tyre" in report_html.lower() or "tire" in report_html.lower():
                print(f"   ✅ Contains industry-specific content (tyres/tires)")
            else:
                print(f"   ⚠️  Missing expected industry keywords")

    print("\n" + "=" * 80)
    print("✅ TEST REPORTS GENERATED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nReports saved to: {output_dir}")


if __name__ == "__main__":
    try:
        generate_test_reports()
    except Exception as e:
        print(f"\n❌ REPORT GENERATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
