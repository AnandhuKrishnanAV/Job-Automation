import json
import logging
from typing import Dict, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from ..utils.config import get_mistral_config

logger = logging.getLogger(__name__)

class MistralAIClient:
    """Client for interacting with Mistral AI API."""
    
    def __init__(self):
        config = get_mistral_config()
        self.client = MistralClient(api_key=config["api_key"])
        self.model = "mistral-medium"
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON response from the API."""
        try:
            # Replace escaped underscores with regular underscores
            cleaned_response = response.replace('\\_', '_')
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            raise ValueError("Invalid JSON response from AI model")
    
    def analyze_job_description(self, job_desc: str) -> Dict:
        """
        Analyzes job description to extract key information.
        
        Args:
            job_desc: Job description text
            
        Returns:
            Dictionary containing parsed job details
        """
        try:
            messages = [
                ChatMessage(
                    role="system",
                    content="""You are an expert at analyzing job descriptions and extracting key information.
                    Your task is to analyze the job description and provide structured information that will be used
                    to customize resumes and generate cover letters. Be precise and thorough in your analysis."""
                ),
                ChatMessage(
                    role="user",
                    content=f"""
                    Analyze the following job description and extract key information in JSON format:
                    
                    {job_desc}
                    
                    Please provide a JSON object with the following structure:
                    {{
                        "title": "Job title",
                        "required_skills": ["list", "of", "required", "skills"],
                        "preferred_skills": ["list", "of", "preferred", "skills"],
                        "experience_level": "Required years/level of experience",
                        "education_requirements": ["list", "of", "education", "requirements"],
                        "key_responsibilities": ["list", "of", "main", "responsibilities"],
                        "technical_requirements": ["list", "of", "technical", "requirements"],
                        "soft_skills": ["list", "of", "soft", "skills"],
                        "company_values": ["list", "of", "company", "values"],
                        "industry": "Primary industry",
                        "location": "Job location",
                        "employment_type": "Full-time/Part-time/Contract"
                    }}
                    """
                )
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            return self._parse_json_response(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            raise ValueError("Error analyzing job description: Invalid JSON response")
        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            raise ValueError(f"Error analyzing job description: {str(e)}")
    
    def customize_resume(self, job_details: Dict, current_resume: str) -> str:
        """
        Customizes resume content based on job details.
        
        Args:
            job_details: Dictionary containing job requirements
            current_resume: Current resume content in LaTeX format
            
        Returns:
            Customized resume content in LaTeX format
        """
        try:
            messages = [
                ChatMessage(
                    role="system",
                    content="""You are an expert at customizing resumes to match job requirements.
                    Your task is to modify the provided resume to better match the job requirements
                    while maintaining professionalism and authenticity. Focus on highlighting relevant
                    experience and using industry-specific keywords."""
                ),
                ChatMessage(
                    role="user",
                    content=f"""
                    Please customize the following resume to better match the job requirements.
                    Keep the LaTeX formatting intact and only modify the content.
                    
                    Job Requirements:
                    {json.dumps(job_details, indent=2)}
                    
                    Current Resume:
                    {current_resume}
                    """
                )
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error customizing resume: {e}")
            raise ValueError(f"Error customizing resume: {str(e)}")
    
    def generate_cover_letter(self, job_details: Dict, candidate_info: Dict) -> str:
        """
        Generates a cover letter based on job details.
        
        Args:
            job_details: Dictionary containing job and company information
            candidate_info: Dictionary containing candidate's background and experience
            
        Returns:
            Generated cover letter in LaTeX format
        """
        try:
            messages = [
                ChatMessage(
                    role="system",
                    content="""You are an expert at writing professional cover letters.
                    Your task is to generate a compelling cover letter that highlights the candidate's
                    qualifications and demonstrates their fit for the position."""
                ),
                ChatMessage(
                    role="user",
                    content=f"""
                    Please generate a cover letter in LaTeX format using the following information:
                    
                    Job Details:
                    {json.dumps(job_details, indent=2)}
                    
                    Candidate Information:
                    {json.dumps(candidate_info, indent=2)}
                    """
                )
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            raise ValueError(f"Error generating cover letter: {str(e)}")
    
    def suggest_improvements(self, resume_content: str) -> List[str]:
        """
        Suggests improvements for a resume.
        
        Args:
            resume_content: Current resume content
            
        Returns:
            List of suggested improvements
        """
        try:
            messages = [
                ChatMessage(
                    role="system",
                    content="""You are an expert at reviewing resumes and providing constructive feedback.
                    Your task is to analyze the resume and suggest specific improvements that would make
                    it more effective and professional."""
                ),
                ChatMessage(
                    role="user",
                    content=f"""
                    Please review the following resume and provide a list of specific improvements:
                    
                    {resume_content}
                    """
                )
            ]
            
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            suggestions = response.choices[0].message.content.split("\n")
            return [s.strip() for s in suggestions if s.strip()]
        except Exception as e:
            logger.error(f"Error suggesting improvements: {e}")
            raise ValueError(f"Error suggesting improvements: {str(e)}")
