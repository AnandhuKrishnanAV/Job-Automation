from setuptools import setup, find_packages

setup(
    name="job_application_automator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mistralai==0.0.9",
        "python-dotenv>=1.0.0",
        "SQLAlchemy>=2.0.0",
        "pytest>=8.0.0",
        "Jinja2>=3.0.0",
        "schedule>=1.2.0",
        "pdflatex>=0.1.3",
    ],
    entry_points={
        "console_scripts": [
            "job-automator=job_application_automator.cli:main",
        ],
    },
    author="Anandhu Krishnan AV",
    author_email="anandhukrishnanav3@gmail.com",
    description="An AI-powered job application automation tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="job application, automation, AI, resume, cover letter",
    url="https://github.com/yourusername/job_application_automator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
