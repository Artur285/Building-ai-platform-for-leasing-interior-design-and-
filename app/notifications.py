"""
Email notification system for AI Building Materials Leasing Platform.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for sending email notifications."""
    
    def __init__(self, app=None):
        """Initialize email service."""
        self.smtp_host = None
        self.smtp_port = None
        self.smtp_username = None
        self.smtp_password = None
        self.smtp_use_tls = True
        self.from_email = None
        self.enabled = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app configuration."""
        self.smtp_host = os.getenv('SMTP_HOST', app.config.get('SMTP_HOST'))
        self.smtp_port = int(os.getenv('SMTP_PORT', app.config.get('SMTP_PORT', 587)))
        self.smtp_username = os.getenv('SMTP_USERNAME', app.config.get('SMTP_USERNAME'))
        self.smtp_password = os.getenv('SMTP_PASSWORD', app.config.get('SMTP_PASSWORD'))
        self.smtp_use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
        self.from_email = os.getenv('SMTP_FROM_EMAIL', app.config.get('SMTP_FROM_EMAIL'))
        
        # Enable only if all required settings are present
        self.enabled = all([
            self.smtp_host,
            self.smtp_port,
            self.smtp_username,
            self.smtp_password,
            self.from_email
        ])
        
        if self.enabled:
            logger.info("Email notification service enabled")
        else:
            logger.warning("Email notification service disabled - missing configuration")
    
    def send_email(self, to_email: str, subject: str, body_html: str, 
                   body_text: Optional[str] = None, attachments: Optional[List] = None) -> bool:
        """
        Send an email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: HTML body content
            body_text: Plain text body (optional, will be generated from HTML if not provided)
            attachments: List of file paths to attach (optional)
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning("Email service not enabled - cannot send email")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            # Add text body
            if body_text:
                text_part = MIMEText(body_text, 'plain')
                msg.attach(text_part)
            
            # Add HTML body
            html_part = MIMEText(body_html, 'html')
            msg.attach(html_part)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_use_tls:
                    server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_lease_confirmation(self, user_email: str, lease_data: dict) -> bool:
        """Send lease confirmation email."""
        subject = f"Lease Confirmation - {lease_data['project_name']}"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; }}
                .detail {{ margin: 15px 0; padding: 10px; background: white; border-left: 4px solid #667eea; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; 
                          border-radius: 0 0 10px 10px; }}
                .total {{ font-size: 24px; font-weight: bold; color: #667eea; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏗️ Lease Confirmation</h1>
                </div>
                <div class="content">
                    <h2>Your lease has been confirmed!</h2>
                    <p>Thank you for choosing our AI Building Materials Leasing Platform.</p>
                    
                    <div class="detail">
                        <strong>Lease ID:</strong> {lease_data['id']}<br>
                        <strong>Project:</strong> {lease_data['project_name']}<br>
                        <strong>Duration:</strong> {lease_data['start_date']} to {lease_data['end_date']}<br>
                        <strong>Status:</strong> {lease_data['status']}
                    </div>
                    
                    <div class="total">
                        Total Cost: ${lease_data['total_cost']}
                    </div>
                    
                    <h3>Materials Leased:</h3>
                    <ul>
                    {''.join([f"<li>{item['material_name']} - Quantity: {item['quantity']}</li>" 
                              for item in lease_data.get('items', [])])}
                    </ul>
                    
                    <p>Delivery Address: {lease_data.get('delivery_address', 'N/A')}</p>
                </div>
                <div class="footer">
                    <p>AI Building Materials Leasing Platform</p>
                    <p>For questions, contact: support@yourcompany.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_lease_reminder(self, user_email: str, lease_data: dict, days_until_end: int) -> bool:
        """Send lease reminder email."""
        subject = f"Lease Reminder - {lease_data['project_name']} ending in {days_until_end} days"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #f39c12; color: white; padding: 30px; text-align: center; 
                          border-radius: 10px 10px 0 0; }}
                .content {{ background: #fff; padding: 30px; border: 2px solid #f39c12; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #f39c12; padding: 15px; 
                           margin: 20px 0; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; 
                          border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Lease Reminder</h1>
                </div>
                <div class="content">
                    <div class="warning">
                        <strong>Your lease is ending in {days_until_end} days!</strong>
                    </div>
                    
                    <p>Project: <strong>{lease_data['project_name']}</strong></p>
                    <p>Lease ID: {lease_data['id']}</p>
                    <p>End Date: <strong>{lease_data['end_date']}</strong></p>
                    
                    <p>Please ensure all materials are ready for return on or before the end date.</p>
                    
                    <h3>Need to extend your lease?</h3>
                    <p>Contact us to discuss lease extension options.</p>
                </div>
                <div class="footer">
                    <p>AI Building Materials Leasing Platform</p>
                    <p>Contact: support@yourcompany.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_low_inventory_alert(self, admin_email: str, material_name: str, 
                                 quantity_available: int, threshold: int) -> bool:
        """Send low inventory alert to administrators."""
        subject = f"Low Inventory Alert - {material_name}"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #e74c3c; color: white; padding: 30px; text-align: center; 
                          border-radius: 10px 10px 0 0; }}
                .content {{ background: #fff; padding: 30px; border: 2px solid #e74c3c; }}
                .alert {{ background: #ffebee; border-left: 4px solid #e74c3c; padding: 15px; 
                         margin: 20px 0; }}
                .footer {{ background: #2c3e50; color: white; padding: 20px; text-align: center; 
                          border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 Low Inventory Alert</h1>
                </div>
                <div class="content">
                    <div class="alert">
                        <strong>Low inventory detected!</strong>
                    </div>
                    
                    <p><strong>Material:</strong> {material_name}</p>
                    <p><strong>Current Quantity:</strong> {quantity_available}</p>
                    <p><strong>Threshold:</strong> {threshold}</p>
                    
                    <p>Please consider restocking this material to maintain availability.</p>
                    
                    <p><strong>Action Required:</strong> Review inventory and place orders if necessary.</p>
                </div>
                <div class="footer">
                    <p>AI Building Materials Leasing Platform - Admin Alert</p>
                    <p>Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(admin_email, subject, html_body)


# Global instance
email_service = EmailNotificationService()
