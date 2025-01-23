import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict, List
import logging
from datetime import datetime

from ..db.models import EmailTemplate, Session

logger = logging.getLogger(__name__)

class EmailCommunicator:
    """Handles email communication for job applications."""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        if not all([self.smtp_server, self.smtp_port, self.username, self.password]):
            raise ValueError("Missing required email configuration")
    
    def compose_email(self, template: str, details: Dict) -> Dict:
        """
        Composes an email using a template.
        
        Args:
            template: Name of the template to use
            details: Dictionary containing details to fill in template
            
        Returns:
            Dictionary containing email details
        """
        try:
            session = Session()
            email_template = session.query(EmailTemplate).filter_by(name=template).first()
            
            if not email_template:
                raise ValueError(f"Email template '{template}' not found")
            
            content = email_template.content.format(**details)
            subject = email_template.subject.format(**details)
            
            return {
                "to": details.get("to"),
                "subject": subject,
                "body": content,
                "attachments": details.get("attachments", [])
            }
        except Exception as e:
            logger.error(f"Error composing email: {e}")
            raise
        finally:
            session.close()
    
    def send_email(self, email_details: Dict) -> bool:
        """
        Sends an email with attachments.
        
        Args:
            email_details: Dictionary containing email details
            
        Returns:
            Boolean indicating success
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.username
            msg["To"] = email_details["to"]
            msg["Subject"] = email_details["subject"]
            
            msg.attach(MIMEText(email_details["body"], "plain"))
            
            for attachment in email_details.get("attachments", []):
                with open(attachment, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                    part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment)}"'
                    msg.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise
    
    def schedule_email(self, content: Dict, send_date: datetime) -> bool:
        """
        Schedules an email to be sent at a later date.
        
        Args:
            content: Dictionary containing email content
            send_date: Date and time to send the email
            
        Returns:
            Boolean indicating if scheduling was successful
        """
        try:
            # In a real implementation, this would use a task queue like Celery
            # For now, we'll just log it
            logger.info(f"Scheduled email to {content['to']} for {send_date}")
            return True
        except Exception as e:
            logger.error(f"Error scheduling email: {e}")
            raise
