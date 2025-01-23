import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

def get_mistral_config() -> Dict:
    """
    Gets Mistral AI API configuration.
    
    Returns:
        Dictionary containing API configuration
    """
    return {
        "api_key": os.getenv("MISTRAL_API_KEY")
    }

def get_overleaf_config() -> Dict:
    """
    Gets Overleaf API configuration.
    
    Returns:
        Dictionary containing API configuration
    """
    return {
        "api_key": os.getenv("OVERLEAF_API_KEY"),
        "base_url": os.getenv("OVERLEAF_API_URL", "https://api.overleaf.com/v1")
    }

def get_email_config() -> Dict:
    """
    Gets email configuration.
    
    Returns:
        Dictionary containing email configuration
    """
    return {
        "smtp_host": os.getenv("EMAIL_HOST"),
        "smtp_port": int(os.getenv("EMAIL_PORT", "587")),
        "username": os.getenv("EMAIL_USERNAME"),
        "password": os.getenv("EMAIL_PASSWORD")
    }

def get_database_config() -> Dict:
    """
    Gets database configuration.
    
    Returns:
        Dictionary containing database configuration
    """
    return {
        "url": os.getenv("DATABASE_URL", "sqlite:///job_applications.db")
    }
