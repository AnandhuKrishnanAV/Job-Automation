import pytest
from unittest.mock import patch, MagicMock, call
from job_application_automator.core.latex_handler import LatexDocumentHandler

@pytest.fixture
def latex_handler():
    return LatexDocumentHandler()

def test_create_resume(latex_handler):
    # Test data
    experience = latex_handler.format_entry(
        "Software Engineer",
        "Tech Corp",
        "2020 - Present",
        "\\item Led development of core features\\item Improved system performance by 50%"
    )
    
    content = latex_handler.customize_resume_section("experience", experience)
    
    with patch('subprocess.run') as mock_run, patch('pathlib.Path.exists') as mock_exists:
        mock_run.return_value = MagicMock(returncode=0)
        mock_exists.return_value = True
        pdf_path = latex_handler.create_resume(content)
        
        assert pdf_path.endswith('.pdf')
        assert 'resume' in pdf_path
        assert mock_run.call_count == 2
        mock_run.assert_has_calls([
            call(['pdflatex', '-interaction=nonstopmode', 'resume.tex'], 
                cwd=latex_handler.output_dir, capture_output=True, text=True, check=True),
            call(['pdflatex', '-interaction=nonstopmode', 'resume.tex'], 
                cwd=latex_handler.output_dir, capture_output=True, text=True, check=True)
        ])

def test_create_cover_letter(latex_handler):
    content = {
        "candidate_name": "John Doe",
        "candidate_info": "123 Main St\\\\City, State 12345\\\\(555) 123-4567\\\\john@email.com",
        "recipient_info": "HR Manager\\\\Company Name\\\\456 Corp Ave\\\\Business City, State 67890",
        "letter_content": "Dear Hiring Manager,\\\\\\\\I am writing to express my interest..."
    }
    
    with patch('subprocess.run') as mock_run, patch('pathlib.Path.exists') as mock_exists:
        mock_run.return_value = MagicMock(returncode=0)
        mock_exists.return_value = True
        pdf_path = latex_handler.create_cover_letter(content)
        
        assert pdf_path.endswith('.pdf')
        assert 'cover_letter' in pdf_path
        assert mock_run.call_count == 2
        mock_run.assert_has_calls([
            call(['pdflatex', '-interaction=nonstopmode', 'cover_letter.tex'], 
                cwd=latex_handler.output_dir, capture_output=True, text=True, check=True),
            call(['pdflatex', '-interaction=nonstopmode', 'cover_letter.tex'], 
                cwd=latex_handler.output_dir, capture_output=True, text=True, check=True)
        ])

def test_customize_resume_section(latex_handler):
    section = "experience"
    content = "\\item Lead Developer at Tech Corp"
    
    result = latex_handler.customize_resume_section(section, content)
    
    assert "\\section{Experience}" in result
    assert content in result

def test_format_entry(latex_handler):
    title = "Software Engineer"
    subtitle = "Tech Corp"
    date = "2020 - Present"
    description = "\\item Led development\\item Improved performance"
    
    result = latex_handler.format_entry(title, subtitle, date, description)
    
    assert title in result
    assert subtitle in result
    assert date in result
    assert description in result

def test_invalid_section(latex_handler):
    with pytest.raises(ValueError):
        latex_handler.customize_resume_section("invalid_section", "content")
