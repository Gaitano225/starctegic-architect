from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import tempfile

from app.api import deps
from app.services.report_service import ReportGenerator
from app.api.endpoints.strategy import engine # Reuse engine and logic

router = APIRouter()
report_gen = ReportGenerator()

@router.post("/generate-report")
def generate_report(
    *,
    project_name: str,
    user_name: str,
    answers: dict,
    db: Session = Depends(deps.get_db)
):
    """
    Generate and return a PDF report based on user answers.
    """
    try:
        # 1. Get recommendations
        recommendations = engine.evaluate(answers)
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No recommendations generated for the provided answers."
            )
        
        # 2. Generate PDF in a temporary file
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)
        
        report_gen.generate_pdf(
            project_name=project_name,
            user_name=user_name,
            recommendations=[r.dict() for r in recommendations],
            output_path=temp_path
        )
        
        return FileResponse(
            path=temp_path,
            filename=f"Report_{project_name.replace(' ', '_')}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
