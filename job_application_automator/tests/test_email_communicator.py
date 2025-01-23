import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from job_application_automator.core.email_communicator import EmailCommunicator
from job_application_automator.db.models import EmailTemplate

@pytest.fixture
def email_communicator():
    with patch('job_application_automator.core.email_communicator.get_email_config') as mock_config:
        mock_config.return_value = {
            "smtp_host": "smtp.example.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "password123"
        }
        return EmailCommunicator()

@pytest.fixture
def mock_template():
    template = MagicMock()
    template.content = """
    Dear {{ recipient_name }},
    This is a test email for {{ company_name }}.
    Best regards,
    {{ candidate_name }}
    """
    return template

def test_compose_email(email_communicator, mock_template):
    with patch('job_application_automator.db.models.EmailTemplate.get_by_name') as mock_get:
        mock_get.return_value = mock_template
        details = {
            "recipient_name": "John Smith",
            "company_name": "Tech Corp",
            "candidate_name": "Jane Doe"
        }
        result = email_communicator.compose_email("test_template", details)
        assert "John Smith" in result
        assert "Tech Corp" in result
        assert "Jane Doe" in result

def test_send_email(email_communicator):
    with patch('smtplib.SMTP') as mock_smtp:
        content = {
            "to": "recruiter@company.com",
            "subject": "Job Application",
            "body": "Test email content"
        }
        attachments = []
        
        result = email_communicator.send_email(content, attachments)
        assert result is True
        mock_smtp.assert_called_once_with(
            email_communicator.smtp_host,
            email_communicator.smtp_port
        )

def test_generate_follow_up(email_communicator, mock_template):
    with patch('job_application_automator.db.models.EmailTemplate.get_by_name') as mock_get:
        mock_get.return_value = mock_template
        application = {
            "recipient_name": "HR Manager",
            "company_name": "Tech Corp",
            "candidate_name": "Jane Doe"
        }
        result = email_communicator.generate_follow_up(application)
        assert "HR Manager" in result
        assert "Tech Corp" in result
        assert "Jane Doe" in result

def test_schedule_email(email_communicator):
    content = "Test scheduled email"
    send_date = datetime.now()
    application_id = "123"
    
    with patch('schedule.every') as mock_schedule:
        result = email_communicator.schedule_email(content, send_date, application_id)
        assert result is True
        mock_schedule.assert_called_once()
