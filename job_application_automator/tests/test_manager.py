import pytest
from unittest.mock import Mock, patch, MagicMock
from job_application_automator.core.manager import JobApplicationManager
from job_application_automator.db.models import Application, EmailTemplate

@pytest.fixture
def manager():
    return JobApplicationManager()

@pytest.fixture
def sample_job_details():
    return {
        "company_name": "Test Company",
        "position_title": "Software Engineer",
        "job_description": "We are looking for a Python developer...",
        "required_skills": ["Python", "SQL", "API Development"],
        "experience_level": "3-5 years"
    }

@pytest.fixture
def sample_candidate_info():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "(123) 456-7890",
        "address": "123 Main St, City, State 12345",
        "experience": "5 years of software development",
        "education": "BS in Computer Science"
    }

@pytest.fixture
def mock_db_session():
    with patch('job_application_automator.db.models.Session') as mock_session:
        mock_session.return_value.__enter__.return_value = mock_session.return_value
        mock_template = MagicMock(spec=EmailTemplate)
        mock_template.content = "Dear {{ recipient_name }}, ..."
        mock_session.return_value.query.return_value.filter.return_value.first.return_value = mock_template
        yield mock_session

def test_handle_job_description(manager, sample_job_details):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_response = MagicMock()
        mock_response.messages = [MagicMock(content=str(sample_job_details))]
        mock_client.return_value.chat.return_value = mock_response
        
        with patch("job_application_automator.utils.ai_client.MistralAIClient._parse_json_response") as mock_parse:
            mock_parse.return_value = sample_job_details
            result = manager.handle_job_description("Sample job description")
            assert result == sample_job_details

def test_handle_job_description_error(manager):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_client.return_value.chat.side_effect = Exception("API Error")
        with pytest.raises(Exception) as exc_info:
            manager.handle_job_description("Sample job description")
        assert "Error analyzing job description" in str(exc_info.value)

def test_customize_resume(manager, sample_job_details):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_response = MagicMock()
        mock_response.messages = [MagicMock(content="Modified resume content")]
        mock_client.return_value.chat.return_value = mock_response
        
        with patch("job_application_automator.core.latex_handler.LatexDocumentHandler") as mock_latex:
            mock_latex.return_value.create_resume.return_value = "/path/to/resume.pdf"
            result = manager.customize_resume("Sample job description", "Original resume content")
            assert result == "/path/to/resume.pdf"
            mock_latex.return_value.create_resume.assert_called_once()

def test_customize_resume_error(manager):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_client.return_value.chat.side_effect = Exception("AI Error")
        with pytest.raises(Exception) as exc_info:
            manager.customize_resume("Sample job description", "Original resume content")
        assert "Error customizing resume" in str(exc_info.value)

def test_generate_cover_letter(manager, sample_job_details, sample_candidate_info):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_response = MagicMock()
        mock_response.messages = [MagicMock(content="Generated cover letter")]
        mock_client.return_value.chat.return_value = mock_response
        
        with patch("job_application_automator.core.latex_handler.LatexDocumentHandler") as mock_latex:
            mock_latex.return_value.create_cover_letter.return_value = "/path/to/cover_letter.pdf"
            result = manager.generate_cover_letter(sample_job_details, sample_candidate_info)
            assert result == "/path/to/cover_letter.pdf"
            mock_latex.return_value.create_cover_letter.assert_called_once()

def test_generate_cover_letter_error(manager, sample_job_details, sample_candidate_info):
    with patch("job_application_automator.utils.ai_client.MistralClient") as mock_client:
        mock_client.return_value.chat.side_effect = Exception("AI Error")
        with pytest.raises(Exception) as exc_info:
            manager.generate_cover_letter(sample_job_details, sample_candidate_info)
        assert "Error generating cover letter" in str(exc_info.value)

def test_send_application(manager, mock_db_session):
    email_details = {
        "to": "recruiter@company.com",
        "subject": "Job Application - Software Engineer",
        "body": "Dear Hiring Manager...",
        "attachments": ["resume.pdf", "cover_letter.pdf"]
    }
    
    with patch("job_application_automator.core.email_communicator.EmailCommunicator") as mock_email:
        mock_email.return_value.compose_email.return_value = "Composed email content"
        mock_email.return_value.send_email.return_value = True
        
        result = manager.send_application(email_details)
        assert result is True
        mock_email.return_value.compose_email.assert_called_once()
        mock_email.return_value.send_email.assert_called_once()

def test_send_application_error(manager, mock_db_session):
    email_details = {
        "to": "recruiter@company.com",
        "subject": "Job Application",
        "body": "Dear Hiring Manager...",
        "attachments": ["resume.pdf", "cover_letter.pdf"]
    }
    
    with patch("job_application_automator.core.email_communicator.EmailCommunicator") as mock_email:
        mock_email.return_value.send_email.side_effect = Exception("SMTP Error")
        with pytest.raises(Exception) as exc_info:
            manager.send_application(email_details)
        assert "Error sending application" in str(exc_info.value)
