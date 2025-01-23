from job_application_automator.core.manager import JobApplicationManager

def main():
    # Initialize the manager
    manager = JobApplicationManager()

    # Example job description
    job_desc = """
    Software Engineer Position
    We are looking for a Python developer with 3+ years of experience.
    Skills required: Python, AI/ML, REST APIs
    """

    # Example resume content (in LaTeX format)
    resume_content = r"""
    \documentclass{article}
    \begin{document}
    \section{Experience}
    Your resume content here
    \end{document}
    """

    # Example candidate info
    candidate_info = {
        "name": "Your Name",
        "email": "your.email@example.com",
        "phone": "123-456-7890"
    }

    try:
        # Analyze job description
        job_details = manager.handle_job_description(job_desc)
        print("Job details analyzed successfully")

        # Customize resume
        resume_path = manager.customize_resume(job_desc, resume_content)
        print(f"Resume customized and saved to: {resume_path}")

        # Generate cover letter
        cover_letter_path = manager.generate_cover_letter(job_details, candidate_info)
        print(f"Cover letter generated and saved to: {cover_letter_path}")

        # Prepare email details
        email_details = {
            "to_email": "employer@company.com",
            "subject": f"Application for {job_details.get('position', 'Position')}",
            "attachments": [resume_path, cover_letter_path],
            "candidate_name": candidate_info["name"]
        }

        # Send application
        if manager.send_application(email_details):
            print("Application sent successfully!")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 