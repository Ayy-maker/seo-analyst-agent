#!/usr/bin/env python3
"""
Send test notification to verify email setup
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils.notification_service import notification_service
from dotenv import load_dotenv

load_dotenv()

def main():
    print("\n" + "="*70)
    print("📧 SENDING TEST NOTIFICATION")
    print("="*70)

    recipient = os.getenv('NOTIFICATION_EMAIL', 'abhishekmaharjan3737@gmail.com')

    print(f"\nRecipient: {recipient}")
    print("\nChecking email configuration...")

    # Check if email credentials are configured
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    if not sender_email or not sender_password:
        print("\n❌ EMAIL CREDENTIALS NOT CONFIGURED")
        print("\nTo send email notifications, you need to configure:")
        print("1. SENDER_EMAIL - Your Gmail address")
        print("2. SENDER_PASSWORD - Your Gmail app password")
        print("\n📝 Quick Setup Instructions:")
        print("-" * 70)
        print("\nStep 1: Enable 2-Factor Authentication on your Gmail account")
        print("   • Go to https://myaccount.google.com/security")
        print("   • Enable 2-Step Verification")
        print("\nStep 2: Generate App Password")
        print("   • Go to https://myaccount.google.com/apppasswords")
        print("   • Select 'Mail' and 'Other (Custom name)'")
        print("   • Enter 'SEO Analyst' as the app name")
        print("   • Copy the 16-character password")
        print("\nStep 3: Add credentials to .env file")
        print("   Run these commands:")
        print("   ")
        print("   echo 'SENDER_EMAIL=your-email@gmail.com' >> .env")
        print("   echo 'SENDER_PASSWORD=your-app-password' >> .env")
        print("\nStep 4: Run this script again")
        print("   python send_test_notification.py")
        print("\n" + "="*70)

        # Save notification to file instead
        save_notification_to_file(recipient)
        return

    # Try to send notification
    print(f"\n✅ Email credentials configured")
    print(f"   Sender: {sender_email}")
    print("\n📧 Sending system status notification...")

    success = notification_service.send_system_status(recipient=recipient)

    if success:
        print("\n" + "="*70)
        print("✅ NOTIFICATION SENT SUCCESSFULLY!")
        print("="*70)
        print(f"\nCheck your inbox at: {recipient}")
        print("\nThe email includes:")
        print("   • Production service status")
        print("   • Historical tracking data for all 4 clients")
        print("   • Quick links to dashboard and reports")
        print()
    else:
        print("\n" + "="*70)
        print("❌ FAILED TO SEND NOTIFICATION")
        print("="*70)
        print("\nPlease check:")
        print("   1. Email credentials are correct")
        print("   2. Gmail app password is valid (not your account password)")
        print("   3. 2-Factor Authentication is enabled on Gmail")
        print("   4. Internet connection is working")
        print()

        # Save notification to file instead
        save_notification_to_file(recipient)


def save_notification_to_file(recipient):
    """Save notification as HTML file if email fails"""
    print("\n📄 Saving notification as HTML file instead...")

    output_dir = Path("outputs/notifications")
    output_dir.mkdir(parents=True, exist_ok=True)

    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    output_file = output_dir / f"notification-{timestamp}.html"

    # Generate notification HTML
    from database import DatabaseManager
    from utils.snapshot_manager import snapshot_manager

    db = DatabaseManager()
    clients = db.get_all_clients()

    snapshot_data = []
    for client in clients:
        count = snapshot_manager.get_snapshot_count(client['id'])
        latest = snapshot_manager.get_latest_snapshot(client['id'])
        snapshot_data.append({
            'name': client['name'],
            'count': count,
            'latest': latest['snapshot_month'] if latest else 'None',
            'clicks': latest.get('total_clicks', 0) if latest else 0,
            'impressions': latest.get('total_impressions', 0) if latest else 0,
            'position': latest.get('avg_position', 0) if latest else 0
        })

    import subprocess
    try:
        result = subprocess.run(['systemctl', 'is-active', 'seo-analyst'],
                              capture_output=True, text=True)
        service_status = result.stdout.strip()
    except:
        service_status = 'unknown'

    try:
        result = subprocess.run(['systemctl', 'is-active', 'seo-snapshot-capture.timer'],
                              capture_output=True, text=True)
        timer_status = result.stdout.strip()
    except:
        timer_status = 'unknown'

    html_content = notification_service._generate_status_html(
        snapshot_data,
        service_status,
        timer_status
    )

    with open(output_file, 'w') as f:
        f.write(html_content)

    print(f"✅ Notification saved: {output_file}")
    print(f"\nYou can view it at:")
    print(f"   https://seo.theprofitplatform.com.au/preview/{output_file}")
    print(f"\nOr open locally:")
    print(f"   file://{output_file.absolute()}")
    print()


if __name__ == '__main__':
    main()
