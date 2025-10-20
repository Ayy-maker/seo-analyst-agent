#!/usr/bin/env python3
"""
Test Service Account Connections
Quick verification script for GSC and GA4 service account setup
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient

def test_file_exists():
    """Check if service account file exists"""
    print("🔍 Checking service account file...")

    sa_path = Path('config/credentials/service_account.json')
    if sa_path.exists():
        print("✅ Service account file: Found")

        # Check permissions
        import stat
        mode = oct(sa_path.stat().st_mode)[-3:]
        if mode == '600':
            print("✅ File permissions: Secure (600)")
        else:
            print(f"⚠️  File permissions: {mode} (should be 600)")
            print("   Fix with: chmod 600 config/credentials/service_account.json")
        return True
    else:
        print("❌ Service account file: NOT FOUND")
        print("   Expected: config/credentials/service_account.json")
        return False

def test_gsc_connection():
    """Test Google Search Console connection"""
    print("\n📊 Testing Google Search Console...")

    try:
        client = GSCAPIClient()

        if client.connect():
            print(f"✅ GSC connected successfully!")
            print(f"   Auth method: {client.auth_method}")

            # List sites
            sites = client.list_sites()
            print(f"   Sites accessible: {len(sites)}")

            if sites:
                print("\n   Your sites:")
                for site in sites:
                    print(f"      - {site}")

                # Try to fetch data from first site
                print(f"\n   Fetching sample data from: {sites[0]}")
                summary = client.get_site_summary(sites[0], days=7)
                print(f"   ✅ Last 7 days:")
                print(f"      Clicks: {summary['total_clicks']:,}")
                print(f"      Impressions: {summary['total_impressions']:,}")
                print(f"      Queries: {summary['total_queries']:,}")
                return True
            else:
                print("   ⚠️  No sites found")
                print("   Make sure service account email is added to GSC")
                return False
        else:
            print("❌ GSC connection failed")
            print("   Check:")
            print("   1. Service account file exists")
            print("   2. Service account email added to GSC")
            print("   3. Permission set to 'Full' in GSC")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ga4_connection():
    """Test Google Analytics 4 connection"""
    print("\n📈 Testing Google Analytics 4...")

    try:
        client = GA4APIClient()

        if not client.property_id:
            print("⚠️  GA4 Property ID not set")
            print("   Set it with:")
            print("   python3 -c \"from integrations.ga4_api_client import ga4_api_client; ga4_api_client.set_property_id('YOUR_PROPERTY_ID')\"")
            return False

        if client.connect():
            print(f"✅ GA4 connected successfully!")
            print(f"   Auth method: {client.auth_method}")
            print(f"   Property: {client.property_id}")

            # Try to fetch data
            print(f"\n   Fetching sample data...")
            summary = client.get_summary_metrics(days=7)
            print(f"   ✅ Last 7 days:")
            print(f"      Users: {summary['total_users']:,}")
            print(f"      Sessions: {summary['total_sessions']:,}")
            print(f"      Page Views: {summary['total_page_views']:,}")
            print(f"      Engagement Rate: {summary['avg_engagement_rate']}%")
            return True
        else:
            print("❌ GA4 connection failed")
            print("   Check:")
            print("   1. Service account file exists")
            print("   2. Service account email added to GA4")
            print("   3. Property ID is correct")
            print("   4. Service account has 'Viewer' role")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 SERVICE ACCOUNT CONNECTION TESTS")
    print("=" * 70)
    print()

    # Test 1: File exists
    if not test_file_exists():
        print("\n❌ Setup incomplete: Service account file missing")
        print("   Upload service_account.json to config/credentials/")
        return False

    # Test 2: GSC
    gsc_ok = test_gsc_connection()

    # Test 3: GA4
    ga4_ok = test_ga4_connection()

    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    print(f"Service Account File: {'✅ OK' if Path('config/credentials/service_account.json').exists() else '❌ Missing'}")
    print(f"GSC Connection:       {'✅ OK' if gsc_ok else '❌ Failed'}")
    print(f"GA4 Connection:       {'✅ OK' if ga4_ok else '❌ Failed'}")
    print()

    if gsc_ok and ga4_ok:
        print("🎉 ALL TESTS PASSED!")
        print("   Your service account is fully configured and working!")
        print("   Automation is ready to use!")
    elif gsc_ok:
        print("⚠️  Partially configured")
        print("   GSC works, but GA4 needs setup")
        print("   Set GA4 property ID and grant access")
    elif ga4_ok:
        print("⚠️  Partially configured")
        print("   GA4 works, but GSC needs setup")
        print("   Add service account to GSC with Full permissions")
    else:
        print("❌ Setup incomplete")
        print("   Follow SERVICE_ACCOUNT_SETUP.md for instructions")

    print()
    return gsc_ok and ga4_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
