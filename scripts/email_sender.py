"""
Email Sender - Automatically email PDF reports to clients
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional
import os
from datetime import datetime


class EmailSender:
    """Send professional PDF reports via email"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587,
                 sender_email: str = None, sender_password: str = None):
        """
        Initialize email sender
        
        Args:
            smtp_server: SMTP server (e.g., smtp.gmail.com)
            smtp_port: SMTP port (587 for TLS)
            sender_email: Your email address
            sender_password: Your email password or app password
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = sender_email or os.getenv('SENDER_EMAIL')
        self.sender_password = sender_password or os.getenv('SENDER_PASSWORD')
    
    def send_report(self, 
                   recipient_email: str,
                   pdf_path: str,
                   client_name: str = "Client",
                   subject: str = None,
                   custom_message: str = None) -> bool:
        """
        Send PDF report via email
        
        Args:
            recipient_email: Client's email address
            pdf_path: Path to PDF report
            client_name: Client company name
            subject: Email subject (auto-generated if None)
            custom_message: Custom message body
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("❌ Email credentials not configured")
            print("Set SENDER_EMAIL and SENDER_PASSWORD in .env file")
            return False
        
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            print(f"❌ PDF file not found: {pdf_path}")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject or f"SEO Performance Report - {client_name} - {datetime.now().strftime('%B %Y')}"
        
        # Email body
        body = custom_message or self._default_message(client_name)
        msg.attach(MIMEText(body, 'html'))
        
        # Attach PDF
        try:
            with open(pdf_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                              f'attachment; filename="{pdf_file.name}"')
                msg.attach(part)
        except Exception as e:
            print(f"❌ Failed to attach PDF: {e}")
            return False
        
        # Send email
        try:
            print(f"📧 Sending email to {recipient_email}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def send_batch(self, recipients: List[dict], pdf_path: str) -> dict:
        """
        Send report to multiple recipients
        
        Args:
            recipients: List of dicts with 'email', 'name' keys
            pdf_path: Path to PDF report
            
        Returns:
            Dict with success/failure counts
        """
        results = {'sent': 0, 'failed': 0, 'failed_emails': []}
        
        for recipient in recipients:
            email = recipient.get('email')
            name = recipient.get('name', 'Client')
            
            if self.send_report(email, pdf_path, client_name=name):
                results['sent'] += 1
            else:
                results['failed'] += 1
                results['failed_emails'].append(email)
        
        return results
    
    def _default_message(self, client_name: str) -> str:
        """Generate default email body"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #667eea;">Monthly SEO Performance Report</h2>
            
            <p>Dear {client_name} Team,</p>
            
            <p>Please find attached your comprehensive SEO performance report for this month.</p>
            
            <p><strong>This report includes:</strong></p>
            <ul>
                <li>📊 SEO Health Score & KPI Dashboard</li>
                <li>🔍 Keywords Analysis (rankings, CTR, opportunities)</li>
                <li>🔧 Technical SEO Audit</li>
                <li>📝 On-Page Optimization Recommendations</li>
                <li>🔗 Backlinks Profile Analysis</li>
                <li>📈 Traffic & Conversion Insights</li>
                <li>💡 Prioritized Action Plan</li>
            </ul>
            
            <p><strong>Key Highlights:</strong></p>
            <p>Review the executive summary on page 1 for immediate insights and critical issues requiring attention.</p>
            
            <p>If you have any questions or would like to discuss these findings, please don't hesitate to reach out.</p>
            
            <p>Best regards,<br>
            <strong>Your SEO Team</strong></p>
            
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #999;">
                This is an automated report generated by SEO Analyst Agent.<br>
                Report Date: {datetime.now().strftime('%B %d, %Y')}
            </p>
        </body>
        </html>
        """


# CLI usage
if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Send SEO report via email')
    parser.add_argument('--pdf', required=True, help='Path to PDF report')
    parser.add_argument('--to', required=True, help='Recipient email')
    parser.add_argument('--client', default='Client', help='Client name')
    parser.add_argument('--subject', help='Email subject')
    
    args = parser.parse_args()
    
    sender = EmailSender()
    success = sender.send_report(
        recipient_email=args.to,
        pdf_path=args.pdf,
        client_name=args.client,
        subject=args.subject
    )
    
    sys.exit(0 if success else 1)
