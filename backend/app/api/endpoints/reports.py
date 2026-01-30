from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import tempfile

from app.api import deps
from app.services.report_service import ReportGenerator
from app.services.validator_service import PreFlightValidator
from app.api.endpoints.strategy import engine # Reuse engine and logic

router = APIRouter()
report_gen = ReportGenerator()

from pydantic import BaseModel

class ReportRequest(BaseModel):
    project_name: Optional[str] = "Mon Projet"
    user_name: Optional[str] = "Utilisateur"
    answers: Dict[str, Any] = {}

@router.post("/generate-report")
async def generate_report(
    *,
    request: ReportRequest,
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user)
):
    """
    Generate and return a professional PDF report (V2) with AI and Finance data.
    Requires an active subscription.
    """
    # 0. Check subscription
    if not current_user.subscription or not current_user.subscription.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Abonnement actif requis pour générer le rapport. Veuillez choisir un plan."
        )
    
    if current_user.subscription.reports_generated >= current_user.subscription.reports_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Limite de rapports atteinte pour votre plan actuel."
        )

    project_name = request.project_name
    user_name = request.user_name
    answers = request.answers
    
    # 0.5 Pre-flight validation (F10)
    warnings = PreFlightValidator.validate(answers)
    if warnings:
        # For now, we just log or could pass to report_gen
        # In a real UI, this would be blocked or shown as warnings
        print(f"PRE-FLIGHT WARNINGS for {project_name}: {warnings}")

    try:
        # 1. Get recommendations
        evaluation_result = engine.evaluate(answers)
        recommendations = evaluation_result["recommendations"]
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No recommendations generated for the provided answers."
            )
        
        # 1.5 Get user plan for content gating
        user_plan = current_user.subscription.plan.value if current_user.subscription else "FOUNDER"
        
        # 2. Generate PDF in a temporary file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"Report_{project_name.replace(' ', '_')}.pdf")
        
        success_path = await report_gen.generate_full_report(
            project_name=project_name,
            user_name=user_name,
            context=answers,
            recommendations=recommendations,
            output_path=temp_path,
            user_plan=user_plan
        )
        
        if success_path:
            # Increment reports count
            current_user.subscription.reports_generated += 1
            db.commit()

            # Trigger Notification for Admin
            from app.services.notification_service import NotificationService
            NotificationService.notify_admin(
                db, 
                "Téléchargement BCT", 
                f"L'utilisateur {current_user.email} a généré un BCT pour le projet: {project_name}."
            )
            
            # Notification pour l'utilisateur
            NotificationService.create_notification(
                db,
                user_id=current_user.id,
                title="Business Case Technique Généré",
                message=f"Votre BCT pour le projet '{project_name}' est prêt ! Il a été généré avec succès et est maintenant disponible au téléchargement. Rapports restants ce mois : {current_user.subscription.reports_limit - current_user.subscription.reports_generated if current_user.subscription.reports_limit < 9999 else 'illimité'}."
            )
            
            return FileResponse(
                path=success_path,
                filename=os.path.basename(success_path),
                media_type="application/pdf" if success_path.endswith(".pdf") else "text/html"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate report file.")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
