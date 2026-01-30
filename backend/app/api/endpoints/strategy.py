import json
import os
from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.rules.engine import RulesEngine
from app.models.project import Project
# from app.models.user import User  # Supprimé pour éviter import circulaire
from app.core.config import settings

router = APIRouter()

# Initialize Rules Engine
RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rules", "base_rules.yaml")
QUESTIONNAIRE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rules", "questionnaire.json")

engine = RulesEngine(RULES_PATH)

@router.post("/questions")
def get_questions(
    current_answers: Dict[str, Any] = {}
) -> Any:
    """
    Get the list of strategic questions, filtered by adaptive logic.
    Example: If an answer implies no mobile app, mobile-specific questions are hidden.
    """
    try:
        with open(QUESTIONNAIRE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_questions = data.get("questions", [])
            
            filtered_questions = []
            for q in all_questions:
                condition = q.get("condition")
                if not condition:
                    filtered_questions.append(q)
                    continue
                
                # Simple evaluation of condition against current_answers
                try:
                    if eval(condition, {"__builtins__": None}, current_answers):
                        filtered_questions.append(q)
                except:
                    # In case of error (e.g. missing key), we skip it to be safe
                    # Small hack: if q14 is about mobile app, and q15 needs q14 == True
                    pass
            
            return {"questions": filtered_questions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading questionnaire: {e}",
        )

from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    project_name: Optional[str] = "Mon Projet"
    answers: Dict[str, Any] = {}

@router.post("/evaluate")
def evaluate_project(
    *,
    db: Session = Depends(deps.get_db),
    request: EvaluationRequest,
    current_user: Any = Depends(deps.get_current_user_optional)
) -> Any:
    from app.models.user import User  # Import local
    """
    Evaluation of project answers and return recommendations.
    Saves the project to the DB if the user is authenticated.
    """
    project_name = request.project_name or "Nouveau Projet"
    answers = request.answers
    
    # Run Inference Engine
    evaluation_result = engine.evaluate(answers)
    recommendations = evaluation_result["recommendations"]
    applied_rule_ids = evaluation_result["applied_rule_ids"]
    
    # Trigger Notifications for Admin
    from app.services.notification_service import NotificationService
    user_email = current_user.email if current_user else "Anonyme"
    NotificationService.notify_admin(
        db, 
        "Lancement Analyse BCT", 
        f"Projet: {project_name} | Utilisateur: {user_email} | Pays: {answers.get('target_country')} | Questions répondues: {len(answers)}"
    )
    
    # Notification pour l'utilisateur connecté
    if current_user:
        NotificationService.create_notification(
            db,
            user_id=current_user.id,
            title="Analyse Stratégique Terminée",
            message=f"Votre projet '{project_name}' a été analysé avec succès. {len(recommendations)} recommandations architecturales ont été générées. Vous pouvez maintenant générer votre Business Case Technique complet."
        )

    project_id = None
    if current_user:
        # Save project to DB with audit trail
        project = Project(
            name=project_name,
            answers=answers,
            recommendations=recommendations,
            applied_rule_ids=applied_rule_ids,
            user_id=current_user.id
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = project.id
    
    return {
        "id": project_id,
        "project_name": project_name,
        "recommendations": recommendations,
        "applied_rule_ids": applied_rule_ids,
        "count": len(recommendations)
    }
