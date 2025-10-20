#!/usr/bin/env python3
"""
Test Phase 1 Improvements - Industry Detection & Demo Data Generation
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
# Import directly from module files to avoid matplotlib dependency
sys.path.insert(0, str(Path(__file__).parent / 'utils'))
from industry_detector import industry_detector
from demo_data_generator import demo_data_generator

def test_industry_detection():
    """Test industry detection with various company names"""
    print("=" * 80)
    print("TESTING INDUSTRY DETECTION")
    print("=" * 80)

    test_companies = [
        "Hot Tyres Sydney",
        "Smith & Partners Legal Services",
        "Bright Smile Dental Clinic Perth",
        "Sydney Property Experts",
        "The Italian Restaurant Melbourne",
        "FitLife Gym Brisbane",
        "Beauty Salon Adelaide",
        "CloudTech Solutions",
        "ABC Retail Store",
        "Just A Company"
    ]

    for company in test_companies:
        industry = industry_detector.detect_industry(company)
        context = industry_detector.get_industry_context(industry)
        location = industry_detector.get_location_from_name(company)

        print(f"\n{company}:")
        print(f"  Industry: {industry}")
        print(f"  Description: {context['description']}")
        print(f"  Location: {location or 'Not detected'}")
        print(f"  Local Important: {context['local_important']}")
        print(f"  Mobile Dominant: {context['mobile_dominant']}")
        print(f"  Expected CTR: {context['avg_ctr']*100:.1f}%")
        print(f"  Typical Position: {context['typical_position']}")


def test_demo_data_generation():
    """Test demo data generation for various industries"""
    print("\n" + "=" * 80)
    print("TESTING DEMO DATA GENERATION")
    print("=" * 80)

    test_cases = [
        ("automotive", "Sydney"),
        ("legal", "Melbourne"),
        ("healthcare", "Perth"),
        ("restaurant", "Brisbane")
    ]

    for industry, location in test_cases:
        print(f"\n{industry.upper()} - {location}:")
        print("-" * 40)

        # Generate keywords
        keywords = demo_data_generator.generate_keywords(industry, location, count=5)
        print(f"\nTop 5 Keywords:")
        for i, kw in enumerate(keywords, 1):
            print(f"  {i}. {kw['query']}")
            print(f"     Clicks: {kw['clicks']}, CTR: {kw['ctr']}%, Position: {kw['position']}, Intent: {kw['intent']}")

        # Generate complete dataset
        dataset = demo_data_generator.generate_complete_dataset(industry, location)

        print(f"\nTotals:")
        print(f"  Total Clicks: {dataset['totals']['clicks']}")
        print(f"  Total Impressions: {dataset['totals']['impressions']:,}")
        print(f"  Average CTR: {dataset['totals']['ctr']}%")
        print(f"  Average Position: {dataset['totals']['avg_position']}")

        print(f"\nDevice Distribution:")
        print(f"  Mobile: {dataset['devices']['mobile']}%")
        print(f"  Desktop: {dataset['devices']['desktop']}%")
        print(f"  Tablet: {dataset['devices']['tablet']}%")

        print(f"\nLanding Pages:")
        for page in dataset['landing_pages'][:3]:
            print(f"  {page['url']} - {page['clicks']} clicks")


def test_integration():
    """Test full integration - company name to complete dataset"""
    print("\n" + "=" * 80)
    print("TESTING FULL INTEGRATION")
    print("=" * 80)

    company_name = "Hot Tyres Sydney"

    # Detect industry
    industry = industry_detector.detect_industry(company_name)
    location = industry_detector.get_location_from_name(company_name) or 'Sydney'

    print(f"\nCompany: {company_name}")
    print(f"Detected Industry: {industry}")
    print(f"Detected Location: {location}")

    # Generate complete dataset
    dataset = demo_data_generator.generate_complete_dataset(industry, location)

    print(f"\n✅ Generated Complete Dataset:")
    print(f"   - {len(dataset['keywords'])} keywords")
    print(f"   - {len(dataset['landing_pages'])} landing pages")
    print(f"   - {len(dataset['historical'])} months of historical data")
    print(f"   - Device distribution: Mobile {dataset['devices']['mobile']}%")

    print(f"\nSample Keywords (NO MORE 'sample keyword X'):")
    for kw in dataset['keywords'][:3]:
        print(f"   - \"{kw['query']}\" ({kw['clicks']} clicks, {kw['ctr']}% CTR)")

    print("\n✅ Phase 1 Integration Test PASSED!")


if __name__ == "__main__":
    try:
        test_industry_detection()
        test_demo_data_generation()
        test_integration()

        print("\n" + "=" * 80)
        print("✅ ALL PHASE 1 TESTS PASSED")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
