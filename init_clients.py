#!/usr/bin/env python3
"""
Initialize Clients in Database
Adds clients from clients.json to the database
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import DatabaseManager


def main():
    print("\n" + "="*70)
    print("🏢 INITIALIZING CLIENTS IN DATABASE")
    print("="*70)

    # Load clients configuration
    config_file = Path(__file__).parent / 'config' / 'clients.json'

    if not config_file.exists():
        print(f"\n❌ Configuration file not found: {config_file}")
        return

    with open(config_file, 'r') as f:
        clients_config = json.load(f)

    print(f"\nFound {len(clients_config)} client(s) in configuration")

    # Initialize database
    db = DatabaseManager()

    # Add each client
    added = 0
    existing = 0

    for client_key, config in clients_config.items():
        client_name = config.get('name')
        domain = config.get('domain')
        website = config.get('website', '')

        print(f"\n{client_name}:")
        print(f"   Domain: {domain}")
        print(f"   Website: {website}")

        # Check if client exists
        existing_client = db.get_client(name=client_name)

        if existing_client:
            print(f"   ℹ️  Already exists (ID: {existing_client['id']})")
            existing += 1
        else:
            # Create client
            client_id = db.create_client(
                name=client_name,
                domain=domain,
                industry=None  # Will be detected by AI
            )
            print(f"   ✅ Created (ID: {client_id})")
            added += 1

    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"\nTotal Clients: {len(clients_config)}")
    print(f"✅ Added: {added}")
    print(f"ℹ️  Already Existing: {existing}")

    # List all clients
    print("\n" + "="*70)
    print("📋 ALL CLIENTS IN DATABASE")
    print("="*70)

    all_clients = db.get_all_clients()
    for client in all_clients:
        print(f"\n{client['name']} (ID: {client['id']})")
        print(f"   Domain: {client.get('domain', 'N/A')}")
        print(f"   Created: {client.get('created_at', 'N/A')}")

    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
