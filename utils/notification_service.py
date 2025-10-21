"""
Notification Service - Send email notifications for system events
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class NotificationService:
    """Handle email notifications for SEO Analyst system"""

    def __init__(self):
        """Initialize notification service with email configuration"""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL', 'abhishekmaharjan3737@gmail.com')

    def send_notification(self,
                         subject: str,
                         message: str,
                         recipient: str = None,
                         html: bool = True) -> bool:
        """
        Send email notification

        Args:
            subject: Email subject
            message: Email message body (HTML or plain text)
            recipient: Recipient email (uses NOTIFICATION_EMAIL if not specified)
            html: Whether message is HTML (default True)

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("❌ Email credentials not configured")
            print("Please set SENDER_EMAIL and SENDER_PASSWORD in .env file")
            return False

        recipient = recipient or self.notification_email

        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = f"[SEO Analyst] {subject}"

        # Attach message body
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(message, content_type))

        # Send email
        try:
            print(f"📧 Sending notification to {recipient}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Notification sent successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")
            return False

    def send_system_status(self, recipient: str = None) -> bool:
        """
        Send system status notification

        Args:
            recipient: Recipient email (uses NOTIFICATION_EMAIL if not specified)

        Returns:
            True if sent successfully
        """
        from database import DatabaseManager
        from utils.snapshot_manager import snapshot_manager

        db = DatabaseManager()
        clients = db.get_all_clients()

        # Get snapshot status
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

        # Check service status
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

        # Generate HTML message
        html_message = self._generate_status_html(
            snapshot_data,
            service_status,
            timer_status
        )

        subject = f"System Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        return self.send_notification(subject, html_message, recipient)

    def send_snapshot_notification(self,
                                  client_name: str,
                                  snapshot_data: dict,
                                  recipient: str = None) -> bool:
        """
        Send notification when snapshot is captured

        Args:
            client_name: Client name
            snapshot_data: Snapshot metrics
            recipient: Recipient email

        Returns:
            True if sent successfully
        """
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #667eea;">📊 Monthly Snapshot Captured</h2>

                <p>A new monthly snapshot has been captured for <strong>{client_name}</strong>.</p>

                <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2d3748;">Snapshot Metrics</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0;"><strong>Month:</strong></td>
                            <td>{snapshot_data.get('snapshot_month', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Total Clicks:</strong></td>
                            <td>{snapshot_data.get('total_clicks', 0):,}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Total Impressions:</strong></td>
                            <td>{snapshot_data.get('total_impressions', 0):,}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Avg Position:</strong></td>
                            <td>{snapshot_data.get('avg_position', 0):.1f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>CTR:</strong></td>
                            <td>{snapshot_data.get('avg_ctr', 0):.2f}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Total Users:</strong></td>
                            <td>{snapshot_data.get('total_users', 0):,}</td>
                        </tr>
                    </table>
                </div>

                <p style="margin-top: 20px; font-size: 12px; color: #718096;">
                    <em>Automated notification from SEO Analyst Agent</em><br>
                    <em>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</em>
                </p>
            </div>
        </body>
        </html>
        """

        subject = f"Monthly Snapshot Captured - {client_name}"

        return self.send_notification(subject, html_message, recipient)

    def send_report_notification(self,
                                client_name: str,
                                report_path: str,
                                recipient: str = None) -> bool:
        """
        Send notification when report is generated

        Args:
            client_name: Client name
            report_path: Path to generated report
            recipient: Recipient email

        Returns:
            True if sent successfully
        """
        report_file = Path(report_path)
        report_url = f"https://seo.theprofitplatform.com.au/preview/{report_path}"

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #667eea;">📄 New Report Generated</h2>

                <p>A new SEO report has been generated for <strong>{client_name}</strong>.</p>

                <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Report Details:</strong></p>
                    <ul style="list-style: none; padding-left: 0;">
                        <li>📁 <strong>Filename:</strong> {report_file.name}</li>
                        <li>📊 <strong>Size:</strong> {report_file.stat().st_size / 1024:.1f} KB</li>
                        <li>🕐 <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                    </ul>

                    <p style="margin-top: 20px;">
                        <a href="{report_url}"
                           style="display: inline-block; background: #667eea; color: white;
                                  padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                            📊 View Report
                        </a>
                    </p>
                </div>

                <p style="margin-top: 20px; font-size: 12px; color: #718096;">
                    <em>Automated notification from SEO Analyst Agent</em>
                </p>
            </div>
        </body>
        </html>
        """

        subject = f"SEO Report Generated - {client_name}"

        return self.send_notification(subject, html_message, recipient)

    def _generate_status_html(self,
                             snapshot_data: List[dict],
                             service_status: str,
                             timer_status: str) -> str:
        """Generate HTML for system status notification"""

        # Build snapshot table rows
        snapshot_rows = ""
        for client in snapshot_data:
            snapshot_rows += f"""
                <tr style="border-bottom: 1px solid #e2e8f0;">
                    <td style="padding: 12px;">{client['name']}</td>
                    <td style="padding: 12px;">{client['count']}</td>
                    <td style="padding: 12px;">{client['latest']}</td>
                    <td style="padding: 12px;">{client['clicks']:,}</td>
                    <td style="padding: 12px;">{client['impressions']:,}</td>
                    <td style="padding: 12px;">{client['position']:.1f}</td>
                </tr>
            """

        service_emoji = "🟢" if service_status == 'active' else "🔴"
        timer_emoji = "🟢" if timer_status == 'active' else "🔴"

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; background-color: #f7fafc;">
            <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                <div style="background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden;">

                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">🚀 SEO Analyst System Status</h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">
                            {datetime.now().strftime('%A, %B %d, %Y at %H:%M UTC')}
                        </p>
                    </div>

                    <!-- Service Status -->
                    <div style="padding: 30px;">
                        <h2 style="color: #2d3748; margin-top: 0;">🔧 Production Services</h2>
                        <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 10px 0;"><strong>SEO Analyst Service:</strong></td>
                                    <td style="text-align: right;">{service_emoji} {service_status.upper()}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px 0;"><strong>Snapshot Scheduler:</strong></td>
                                    <td style="text-align: right;">{timer_emoji} {timer_status.upper()}</td>
                                </tr>
                            </table>
                        </div>

                        <!-- Snapshot Data -->
                        <h2 style="color: #2d3748;">📊 Historical Tracking Status</h2>
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden;">
                                <thead>
                                    <tr style="background: #667eea; color: white;">
                                        <th style="padding: 12px; text-align: left;">Client</th>
                                        <th style="padding: 12px; text-align: left;">Snapshots</th>
                                        <th style="padding: 12px; text-align: left;">Latest</th>
                                        <th style="padding: 12px; text-align: left;">Clicks</th>
                                        <th style="padding: 12px; text-align: left;">Impressions</th>
                                        <th style="padding: 12px; text-align: left;">Position</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {snapshot_rows}
                                </tbody>
                            </table>
                        </div>

                        <!-- System URLs -->
                        <div style="margin-top: 30px; padding: 20px; background: #f7fafc; border-radius: 8px;">
                            <h3 style="color: #2d3748; margin-top: 0;">🌐 Quick Links</h3>
                            <ul style="list-style: none; padding: 0;">
                                <li style="margin: 10px 0;">
                                    <a href="https://seo.theprofitplatform.com.au"
                                       style="color: #667eea; text-decoration: none;">
                                        📊 SEO Analyst Dashboard
                                    </a>
                                </li>
                                <li style="margin: 10px 0;">
                                    <a href="https://seo.theprofitplatform.com.au/preview/outputs/html-reports/"
                                       style="color: #667eea; text-decoration: none;">
                                        📁 View Reports
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div style="background: #2d3748; color: white; padding: 20px; text-align: center;">
                        <p style="margin: 0; font-size: 12px;">
                            Automated notification from SEO Analyst Agent<br>
                            Production URL: <a href="https://seo.theprofitplatform.com.au"
                                              style="color: #667eea;">seo.theprofitplatform.com.au</a>
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return html


# Global instance
notification_service = NotificationService()


# CLI usage
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send system notification')
    parser.add_argument('--status', action='store_true', help='Send system status notification')
    parser.add_argument('--to', help='Recipient email (optional)')

    args = parser.parse_args()

    if args.status:
        notification_service.send_system_status(recipient=args.to)
