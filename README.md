# Job Application Automator

An AI-powered tool to automate and optimize your job application process. Uses Mistral AI to analyze job descriptions, customize resumes, and generate cover letters.

## Features

- Analyze job descriptions to extract key requirements and responsibilities
- Customize your resume based on job requirements
- Generate tailored cover letters
- Get suggestions for resume improvements
- Email integration for sending applications
- Database storage for tracking applications

## Installation

### Option 1: Install from source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job_application_automator.git
cd job_application_automator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

### Option 2: Install via pip (coming soon)

```bash
pip install job-application-automator
```

## Configuration

1. Create a `.env` file in the root directory with your configuration:
```env
MISTRAL_API_KEY=your_mistral_api_key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
DATABASE_URL=sqlite:///applications.db
```

2. Make sure you have LaTeX installed for PDF generation:
- macOS: `brew install mactex`
- Linux: `sudo apt-get install texlive-full`
- Windows: Install MiKTeX from https://miktex.org/

## Usage

The tool can be used via command line interface:

### Analyze a Job Description

```bash
job-automator analyze job_description.txt
```

### Customize Resume

```bash
job-automator customize job_description.txt resume.tex --output customized_resume.tex
```

### Generate Cover Letter

```bash
job-automator cover job_description.txt resume.tex --output cover_letter.tex
```

### Get Resume Suggestions

```bash
job-automator suggest resume.tex
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on the GitHub repository.
