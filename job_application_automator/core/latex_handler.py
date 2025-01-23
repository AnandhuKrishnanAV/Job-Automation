import os
from pathlib import Path
import subprocess
import logging
from typing import Dict, Union

logger = logging.getLogger(__name__)

class LatexDocumentHandler:
    """Handles LaTeX document generation."""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path(__file__).parent.parent / "output"
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_resume(self, content: Union[str, Dict[str, str]]) -> str:
        """
        Creates a resume using the local LaTeX template.
        
        Args:
            content: Either a string containing LaTeX content or a dictionary with resume sections
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Read template
            template_path = self.templates_dir / "resume_template.tex"
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            # If content is a string, use it directly
            if isinstance(content, str):
                latex_content = content
            else:
                # Replace template variables using safe substitution
                latex_content = template_content
                for key, value in content.items():
                    placeholder = f"\\{{{key}}}"
                    latex_content = latex_content.replace(placeholder, value)
            
            # Write to temporary file
            temp_tex_path = self.output_dir / "resume.tex"
            with open(temp_tex_path, 'w') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF
            subprocess.run(['pdflatex', '-output-directory', str(self.output_dir), str(temp_tex_path)], check=True)
            
            return str(self.output_dir / "resume.pdf")
        except Exception as e:
            logger.error(f"Error creating resume: {e}")
            raise ValueError(f"Error creating resume: {str(e)}")
    
    def create_cover_letter(self, content: Union[str, Dict[str, str]]) -> str:
        """
        Creates a cover letter using the local LaTeX template.
        
        Args:
            content: Either a string containing LaTeX content or a dictionary with cover letter sections
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Read template
            template_path = self.templates_dir / "cover_letter_template.tex"
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            # If content is a string, use it directly
            if isinstance(content, str):
                latex_content = content
            else:
                # Replace template variables using safe substitution
                latex_content = template_content
                for key, value in content.items():
                    placeholder = f"\\{{{key}}}"
                    latex_content = latex_content.replace(placeholder, value)
            
            # Write to temporary file
            temp_tex_path = self.output_dir / "cover_letter.tex"
            with open(temp_tex_path, 'w') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF
            subprocess.run(['pdflatex', '-output-directory', str(self.output_dir), str(temp_tex_path)], check=True)
            
            return str(self.output_dir / "cover_letter.pdf")
        except Exception as e:
            logger.error(f"Error creating cover letter: {e}")
            raise ValueError(f"Error creating cover letter: {str(e)}")
    
    def compile_latex(self, content: str, output_name: str) -> str:
        """
        Compiles LaTeX content to PDF.
        
        Args:
            content: LaTeX content
            output_name: Name for the output file (without extension)
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Write to temporary file
            temp_tex_path = self.output_dir / f"{output_name}.tex"
            with open(temp_tex_path, 'w') as f:
                f.write(content)
            
            # Compile LaTeX to PDF
            subprocess.run(['pdflatex', '-output-directory', str(self.output_dir), str(temp_tex_path)], check=True)
            
            return str(self.output_dir / f"{output_name}.pdf")
        except Exception as e:
            logger.error(f"Error compiling LaTeX: {e}")
            raise ValueError(f"Error compiling LaTeX: {str(e)}")
