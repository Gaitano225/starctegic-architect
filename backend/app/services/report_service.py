import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from typing import List, Dict, Any

class ReportGenerator:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.template = self.env.get_template("report.html")

    def generate_pdf(self, project_name: str, user_name: str, recommendations: List[Dict[str, Any]], output_path: str):
        """
        Generate a professional PDF report.
        """
        html_content = self.template.render(
            project_name=project_name,
            user_name=user_name,
            recommendations=recommendations,
            date=datetime.now().strftime("%d/%m/%Y")
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        return output_path
