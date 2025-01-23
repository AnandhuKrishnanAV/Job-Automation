#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path
from job_application_automator.core.manager import JobApplicationManager
from job_application_automator.utils.config import get_mistral_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_parser():
    parser = argparse.ArgumentParser(
        description="AI-powered job application automation tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze job description
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a job description")
    analyze_parser.add_argument("job_file", type=str, help="Path to job description file")
    
    # Customize resume
    customize_parser = subparsers.add_parser("customize", help="Customize resume for a job")
    customize_parser.add_argument("job_file", type=str, help="Path to job description file")
    customize_parser.add_argument("resume_file", type=str, help="Path to resume file")
    customize_parser.add_argument("--output", "-o", type=str, help="Output path for customized resume")
    
    # Generate cover letter
    cover_parser = subparsers.add_parser("cover", help="Generate a cover letter")
    cover_parser.add_argument("job_file", type=str, help="Path to job description file")
    cover_parser.add_argument("resume_file", type=str, help="Path to resume file")
    cover_parser.add_argument("--output", "-o", type=str, help="Output path for cover letter")
    
    # Suggest improvements
    suggest_parser = subparsers.add_parser("suggest", help="Get resume improvement suggestions")
    suggest_parser.add_argument("resume_file", type=str, help="Path to resume file")
    
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        manager = JobApplicationManager()
        
        if args.command == "analyze":
            with open(args.job_file, 'r') as f:
                job_desc = f.read()
            result = manager.analyze_job_description(job_desc)
            print("\nJob Analysis:")
            for key, value in result.items():
                print(f"\n{key.replace('_', ' ').title()}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                else:
                    print(f"  {value}")
        
        elif args.command == "customize":
            with open(args.job_file, 'r') as f:
                job_desc = f.read()
            with open(args.resume_file, 'r') as f:
                resume = f.read()
            
            customized = manager.customize_resume(job_desc, resume)
            output_path = args.output or "customized_resume.tex"
            with open(output_path, 'w') as f:
                f.write(customized)
            print(f"\nCustomized resume saved to: {output_path}")
        
        elif args.command == "cover":
            with open(args.job_file, 'r') as f:
                job_desc = f.read()
            with open(args.resume_file, 'r') as f:
                resume = f.read()
            
            cover_letter = manager.generate_cover_letter(job_desc, resume)
            output_path = args.output or "cover_letter.tex"
            with open(output_path, 'w') as f:
                f.write(cover_letter)
            print(f"\nCover letter saved to: {output_path}")
        
        elif args.command == "suggest":
            with open(args.resume_file, 'r') as f:
                resume = f.read()
            
            suggestions = manager.suggest_improvements(resume)
            print("\nSuggested Improvements:")
            for suggestion in suggestions:
                print(f"\n- {suggestion}")
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
