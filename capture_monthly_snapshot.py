#!/usr/bin/env python3
"""
Capture Monthly Snapshot
Captures current month's SEO performance for all clients
"""

import os
import sys
from pathlib import Path
from datetime import datetime, date
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from integrations.gsc_api_client import GSCAPIClient
from integrations.ga4_api_client import GA4APIClient
from utils.data_normalizer import data_normalizer
from utils.snapshot_manager import snapshot_manager
from database import DatabaseManager
import json


def capture_client_snapshot(client: dict, snapshot_date: date = None) -> bool:
    """
    Capture snapshot for a single client

    Args:
        client: Client dictionary with configuration
        snapshot_date: Date for snapshot (defaults to today)

    Returns:
        True if successful, False otherwise
    """
    if snapshot_date is None:
        snapshot_date = date.today()

    client_id = client['id']
    client_name = client['name']

    print(f"\n{'='*70}")
    print(f"📸 Capturing snapshot for: {client_name}")
    print(f"{'='*70}")

    # Load client configuration
    config_file = Path(__file__).parent / 'config' / 'clients.json'
    if not config_file.exists():
        print(f"⚠️  No client configuration found at {config_file}")
        return False

    with open(config_file, 'r') as f:
        clients_config = json.load(f)

    # Find client config by name (normalized)
    client_key = client_name.lower().replace(' ', '_').replace('-', '_')
    client_config = None
    for key, config in clients_config.items():
        if key == client_key or config.get('name') == client_name:
            client_config = config
            break

    if not client_config:
        print(f"⚠️  No configuration found for {client_name}")
        return False

    # Get GSC property
    gsc_property = client_config.get('gsc_property')
    if not gsc_property:
        print(f"⚠️  No GSC property configured for {client_name}")
        return False

    # Get GA4 property
    ga4_property_id = client_config.get('ga4_property_id')

    # Fetch GSC data
    print(f"\n1️⃣  Fetching GSC data...")
    print(f"   Property: {gsc_property}")

    try:
        gsc_client = GSCAPIClient()
        if not gsc_client.connect():
            print("   ❌ GSC connection failed")
            return False

        queries = gsc_client.fetch_queries_with_metrics(gsc_property, days=30)
        if not queries:
            print("   ❌ No GSC data available")
            return False

        print(f"   ✅ Fetched {len(queries)} queries")

        # Normalize GSC data
        gsc_parsed = {
            'source': 'Google Search Console',
            'site_url': gsc_property,
            'record_count': len(queries),
            'data': queries
        }
        normalized_gsc = data_normalizer.normalize_gsc_data(gsc_parsed, client_name)

    except Exception as e:
        print(f"   ❌ GSC Error: {e}")
        return False

    # Fetch GA4 data (if configured)
    ga4_data = None
    if ga4_property_id:
        print(f"\n2️⃣  Fetching GA4 data...")
        print(f"   Property ID: {ga4_property_id}")

        try:
            ga4_client = GA4APIClient(property_id=ga4_property_id)
            if not ga4_client.connect():
                print("   ⚠️  GA4 connection failed (continuing without GA4 data)")
            else:
                behavior_data = ga4_client.fetch_user_behavior(days=30)
                if 'error' not in behavior_data:
                    print(f"   ✅ Fetched {behavior_data.get('total_rows', 0)} days of data")

                    # Normalize GA4 data
                    ga4_parsed = {
                        'source': 'Google Analytics 4',
                        'property_id': ga4_property_id,
                        'record_count': behavior_data.get('total_rows', 0),
                        'data': behavior_data.get('data', [])
                    }
                    ga4_data = data_normalizer.normalize_ga4_data(ga4_parsed)
                else:
                    print(f"   ⚠️  GA4 Error: {behavior_data.get('error')} (continuing without GA4)")

        except Exception as e:
            print(f"   ⚠️  GA4 Error: {e} (continuing without GA4 data)")
    else:
        print(f"\n2️⃣  Skipping GA4 (no property ID configured)")

    # Capture snapshot
    print(f"\n3️⃣  Saving snapshot...")
    print(f"   Date: {snapshot_date}")
    print(f"   Month: {snapshot_date.strftime('%Y-%m')}")

    try:
        snapshot_id = snapshot_manager.capture_snapshot(
            client_id=client_id,
            gsc_data=normalized_gsc,
            ga4_data=ga4_data,
            snapshot_date=snapshot_date,
            source='automated'
        )

        print(f"   ✅ Snapshot saved (ID: {snapshot_id})")

        # Show snapshot summary
        latest = snapshot_manager.get_latest_snapshot(client_id)
        if latest:
            print(f"\n   📊 Snapshot Summary:")
            print(f"      Clicks: {latest['total_clicks']:,}")
            print(f"      Impressions: {latest['total_impressions']:,}")
            print(f"      CTR: {latest['avg_ctr']:.2f}%")
            print(f"      Avg Position: {latest['avg_position']:.1f}")
            if latest['total_users'] > 0:
                print(f"      Users: {latest['total_users']:,}")
                print(f"      Sessions: {latest['total_sessions']:,}")

            # Show changes (if available)
            if latest['clicks_change_percent'] is not None:
                print(f"\n   📈 Changes vs Previous Month:")
                print(f"      Clicks: {latest['clicks_change_percent']:+.1f}%")
                print(f"      Impressions: {latest['impressions_change_percent']:+.1f}%")
                if latest['users_change_percent']:
                    print(f"      Users: {latest['users_change_percent']:+.1f}%")

        return True

    except Exception as e:
        print(f"   ❌ Snapshot failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Capture snapshots for all clients"""
    print("\n" + "="*70)
    print("📸 MONTHLY SNAPSHOT CAPTURE")
    print("="*70)

    snapshot_date = date.today()
    print(f"\nSnapshot Date: {snapshot_date}")
    print(f"Snapshot Month: {snapshot_date.strftime('%B %Y')}")

    # Get all clients
    db = DatabaseManager()
    clients = db.get_all_clients()

    if not clients:
        print("\n❌ No clients found in database")
        print("   Add clients via web interface first")
        return

    print(f"\nFound {len(clients)} client(s)")

    # Capture snapshot for each client
    successful = 0
    failed = 0

    for client in clients:
        try:
            if capture_client_snapshot(client, snapshot_date):
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Unexpected error for {client['name']}: {e}")
            failed += 1

    # Summary
    print("\n" + "="*70)
    print("📊 CAPTURE SUMMARY")
    print("="*70)
    print(f"\nTotal Clients: {len(clients)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")

    # Show historical data status
    print("\n" + "="*70)
    print("📚 HISTORICAL DATA STATUS")
    print("="*70)

    for client in clients:
        count = snapshot_manager.get_snapshot_count(client['id'])
        print(f"\n{client['name']}:")
        print(f"   Total Snapshots: {count}")

        if count > 0:
            latest = snapshot_manager.get_latest_snapshot(client['id'])
            print(f"   Latest: {latest['snapshot_month']}")

            if count >= 2:
                print(f"   ✅ Historical comparison available")
            else:
                print(f"   ⏳ Need 1 more month for comparison")
        else:
            print(f"   ⚠️  No snapshots yet")

    print("\n" + "="*70)
    print("\n💡 Tip: Run this script monthly to build historical data")
    print("   Set up a cron job: 0 0 1 * * /path/to/script (1st of each month)")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
