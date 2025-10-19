#!/usr/bin/env python3
"""
Clean Database Script
Removes demo, sample, and test data
"""

import sys
from pathlib import Path

# Add project to path
sys.path.append(str(Path(__file__).parent.parent))

from database import DatabaseManager

def clean_demo_data():
    """Remove all demo, sample, and test data"""
    db = DatabaseManager()
    
    print("🧹 Cleaning demo data from database...")
    
    # Get all clients
    clients = db.get_all_clients()
    
    removed_count = 0
    for client in clients:
        name = client['name'].lower()
        if any(keyword in name for keyword in ['demo', 'sample', 'test', 'example']):
            print(f"  Removing: {client['name']} (ID: {client['id']})")
            
            # Delete client (cascade will remove related data)
            db.conn.execute("DELETE FROM clients WHERE id = ?", (client['id'],))
            db.conn.commit()
            removed_count += 1
    
    print(f"\n✅ Removed {removed_count} demo clients")
    
    # Show remaining clients
    remaining = db.get_all_clients()
    print(f"📊 Remaining clients: {len(remaining)}")
    
    if remaining:
        print("\nCurrent clients:")
        for client in remaining:
            reports = db.get_reports(client['id'])
            print(f"  • {client['name']} ({len(reports)} reports)")
    else:
        print("  (Database is now clean - ready for real client data)")

if __name__ == '__main__':
    clean_demo_data()
