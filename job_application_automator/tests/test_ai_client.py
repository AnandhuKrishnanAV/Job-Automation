import pytest
import json
from unittest.mock import patch, MagicMock
from job_application_automator.utils.ai_client import MistralAIClient

@pytest.fixture
def ai_client():
    with patch('job_application_automator.utils.ai_client.get_mistral_config') as mock_config:
        mock_config.return_value = {"api_key": "test_key"}
        return MistralAIClient()

@pytest.fixture
def mock_response():
    mock_msg = MagicMock()
    mock_msg.content = json.dumps({
        "title": "Senior Software Engineer",
        "required_skills": ["Python", "Cloud", "Problem-solving"],
        "experience_level": "5+ years"
    })
    
    response = MagicMock()
    response.messages = [mock_msg]
    return response

def test_analyze_job_description(ai_client, mock_response):
    job_desc = """
    Senior Software Engineer
    Requirements:
    - 5+ years of Python experience
    - Experience with cloud platforms
    - Strong problem-solving skills
    """
    
    with patch.object(ai_client.client, 'chat', return_value=mock_response) as mock_chat:
        result = ai_client.analyze_job_description(job_desc)
        
        assert isinstance(result, dict)
        assert result["title"] == "Senior Software Engineer"
        assert "Python" in result["required_skills"]
        
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args[1]
        messages = call_args['messages']
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "expert at analyzing job descriptions" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert job_desc in messages[1]["content"]

def test_customize_resume(ai_client, mock_response):
    job_details = {
        "required_skills": ["Python", "Cloud", "Problem-solving"],
        "experience_level": "Senior",
        "key_responsibilities": ["Lead development", "Mentor junior devs"]
    }
    current_resume = "\\section{Experience}\n\\item Lead Developer at Tech Corp"
    
    # Override mock response for this specific test
    mock_response.messages[0].content = "Modified resume content with highlighted Python and Cloud experience"
    
    with patch.object(ai_client.client, 'chat', return_value=mock_response) as mock_chat:
        result = ai_client.customize_resume(job_details, current_resume)
        
        assert isinstance(result, str)
        assert "Python" in result or "Cloud" in result
        
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args[1]
        messages = call_args['messages']
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        
        # Check if job details are in the message content (allowing for different JSON formatting)
        message_content = messages[1]["content"]
        for skill in job_details["required_skills"]:
            assert skill in message_content
        assert job_details["experience_level"] in message_content
        for resp in job_details["key_responsibilities"]:
            assert resp in message_content
        assert current_resume in message_content

def test_generate_cover_letter(ai_client, mock_response):
    job_details = {
        "company_name": "Tech Corp",
        "position": "Senior Software Engineer",
        "key_requirements": ["Python", "Leadership", "Innovation"]
    }
    candidate_info = {
        "name": "John Doe",
        "experience": "7 years in software development",
        "achievements": ["Led team of 5 developers", "Improved system performance by 50%"]
    }
    
    # Override mock response for this specific test
    mock_response.messages[0].content = "Dear Hiring Manager,\n\nI am writing to express my interest..."
    
    with patch.object(ai_client.client, 'chat', return_value=mock_response) as mock_chat:
        result = ai_client.generate_cover_letter(job_details, candidate_info)
        
        assert isinstance(result, str)
        assert "Dear" in result
        assert "interest" in result
        
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args[1]
        messages = call_args['messages']
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        
        # Check if all required information is in the message content
        message_content = messages[1]["content"]
        assert job_details["company_name"] in message_content
        assert job_details["position"] in message_content
        for req in job_details["key_requirements"]:
            assert req in message_content
        assert candidate_info["name"] in message_content
        assert candidate_info["experience"] in message_content
        for achievement in candidate_info["achievements"]:
            assert achievement in message_content

def test_suggest_improvements(ai_client, mock_response):
    resume_content = "\\section{Experience}\n\\item Software Developer at Tech Corp"
    
    # Override mock response for this specific test
    mock_response.messages[0].content = json.dumps({
        "suggestions": [
            "Add quantifiable achievements",
            "Include technical skills section"
        ],
        "examples": {
            "achievements": "Improved system performance by 50%",
            "skills": "Python, Java, Cloud platforms"
        }
    })
    
    with patch.object(ai_client.client, 'chat', return_value=mock_response) as mock_chat:
        result = ai_client.suggest_improvements(resume_content)
        
        assert isinstance(result, dict)
        assert "suggestions" in result
        assert "examples" in result
        assert len(result["suggestions"]) > 0
        
        mock_chat.assert_called_once()
        call_args = mock_chat.call_args[1]
        messages = call_args['messages']
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert resume_content in messages[1]["content"]

def test_parse_json_response_error(ai_client):
    with pytest.raises(ValueError, match="Invalid JSON response from AI model"):
        ai_client._parse_json_response("invalid json")

def test_api_error_handling(ai_client):
    with patch.object(ai_client.client, 'chat', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            ai_client.analyze_job_description("test job")
        assert "API Error" in str(exc_info.value)
