import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except Exception:
    HAS_WEASYPRINT = False
from typing import List, Dict, Any

from app.services.finance_service import FinanceService
from app.services.ai_service import AIService

class ReportGenerator:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.template = self.env.get_template("report.html")
        self.finance = FinanceService()
        self.ai = AIService()

    async def generate_full_report(self, 
                                   project_name: str, 
                                   user_name: str, 
                                   context: Dict[str, Any],
                                   recommendations: List[Dict[str, Any]],
                                   output_path: str,
                                   user_plan: str = "FOUNDER"):
        """
        Produce a complete V2 Business Case including AI narrative and Finance projections.
        Content is gated based on user subscription plan.
        """
        # 1. Financial simulation
        budget = context.get("budget_amount", 1000000)
        infra_scale = "small" if budget < 5000000 else "medium"
        monthly_infra = self.finance.estimate_infra_monthly_cost(infra_scale)
        finance_data = self.finance.calculate_roi_3years(
            initial_dev_cost=budget * 0.7, # Assuming 70% of budget for dev
            monthly_infra_cost=monthly_infra,
            expected_monthly_revenue=budget * 0.1 # Very rough estimate
        )

        # 2. AI Enhancement with Plan-based Gating
        ai_narrative = await self.ai.enhance_report(
            {"name": project_name, "answers": context}, 
            recommendations,
            user_plan
        )

        # 3. Prepare template data
        report_data = {
            "project_name": project_name,
            "user_name": user_name,
            "date": datetime.now().strftime("%d/%m/%Y"),
            "ai_narrative": ai_narrative,
            "finance": finance_data,
            "recommendations": recommendations,
            "context": context,
            "answers": context, # For template convenience
            "user_plan": user_plan,  # For template conditional rendering
            # Direct access for backwards compatibility
            "problem": context.get("problem_statement", "Non spécifié"),
            "solution": context.get("solution_description", "Non spécifié"),
            "demand": context.get("market_demand", "Non spécifiée"),
            "competitors": context.get("competitor_analysis", "Non spécifiée"),
            "uvp": context.get("unique_value_prop", "Non spécifié"),
            "sector": context.get("sector", "Général"),
            "country": context.get("target_country", "BJ")
        }

        # 4. Render HTML
        html_content = self.template.render(**report_data)
        
        # 4. Save PDF
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if HAS_WEASYPRINT:
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        else:
            # Fallback to HTML file if WeasyPrint is missing
            with open(output_path.replace(".pdf", ".html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            return output_path.replace(".pdf", ".html")
