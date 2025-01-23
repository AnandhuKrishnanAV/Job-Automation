from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

from .latex_handler import LatexDocumentHandler
from .email_communicator import EmailCommunicator
from ..utils.ai_client import MistralAIClient
from ..db.models import Application

logger = logging.getLogger(__name__)

class JobApplicationManager:
    """Manages the entire job application process."""
    
    def __init__(self):
        self.latex_handler = LatexDocumentHandler()
        self.email_communicator = EmailCommunicator()
        self.ai_client = MistralAIClient()
    
    def handle_job_description(self, job_desc: str) -> Dict:
        """
        Analyzes job description and extracts relevant information.
        
        Args:
            job_desc: The job description text
            
        Returns:
            Dict containing parsed job details
        """
        try:
            job_details = self.ai_client.analyze_job_description(job_desc)
            return job_details
        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            raise ValueError(f"Error analyzing job description: {str(e)}")
    
    def customize_resume(self, job_desc: str, resume_content: str) -> str:
        """
        Customizes resume based on job description.
        
        Args:
            job_desc: The job description text
            resume_content: Current resume content in LaTeX format
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # First analyze the job description
            job_details = self.handle_job_description(job_desc)
            
            # Then customize the resume
            customized_resume = self.ai_client.customize_resume(job_details, resume_content)
            return self.latex_handler.create_resume(customized_resume)
        except Exception as e:
            logger.error(f"Error customizing resume: {e}")
            raise ValueError("Error customizing resume")
    
    def generate_cover_letter(self, job_details: Dict, candidate_info: Dict) -> str:
        """
        Generates a cover letter based on job details.
        
        Args:
            job_details: Dictionary containing job and company information
            candidate_info: Dictionary containing candidate's information
            
        Returns:
            Path to the generated PDF file
        """
        try:
            cover_letter_content = self.ai_client.generate_cover_letter(job_details, candidate_info)
            return self.latex_handler.create_cover_letter(cover_letter_content)
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            raise ValueError("Error generating cover letter")
    
    def send_application(self, email_details: Dict) -> bool:
        """
        Sends job application email with attachments.
        
        Args:
            email_details: Dictionary containing email content and attachments
            
        Returns:
            Boolean indicating success
        """
        try:
            email_content = self.email_communicator.compose_email(
                template="application",
                details=email_details
            )
            return self.email_communicator.send_email(email_content)
        except Exception as e:
            logger.error(f"Error sending application: {e}")
            raise ValueError("Error sending application")
    
    def schedule_follow_up(self, application_id: str) -> bool:
        """
        Schedules a follow-up email for an application.
        
        Args:
            application_id: Unique identifier for the application
            
        Returns:
            Boolean indicating if scheduling was successful
        """
        try:
            application = Application.get_by_id(application_id)
            if not application:
                raise ValueError("Application not found")
            
            # Schedule follow-up for 1 week after application
            follow_up_date = datetime.now() + timedelta(days=7)
            
            # Generate follow-up email content
            follow_up_content = self.email_communicator.compose_email(
                template="follow_up",
                details={
                    "company_name": application.company_name,
                    "position": application.position_title,
                    "application_date": application.submission_date.strftime("%Y-%m-%d")
                }
            )
            
            # Schedule the email
            return self.email_communicator.schedule_email(
                content=follow_up_content,
                send_date=follow_up_date
            )
        except Exception as e:
            logger.error(f"Error scheduling follow-up: {e}")
            raise
