import json
import os
from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.rules.engine import RulesEngine
from app.models.project import Project
from app.models.user import User
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

@router.post("/evaluate")
def evaluate_project(
    *,
    db: Session = Depends(deps.get_db),
    project_name: str,
    answers: Dict[str, Any],
    current_user: User = Depends(deps.get_current_user) # Optional auth depends
) -> Any:
    """
    Evaluate project answers and return recommendations.
    Saves the project to the DB if the user is authenticated.
    """
    recommendations = engine.evaluate(answers)
    recs_data = [r.dict() for r in recommendations]
    
    # Save project to DB
    project = Project(
        name=project_name,
        answers=answers,
        recommendations=recs_data,
        user_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "project_name": project_name,
        "recommendations": recommendations,
        "count": len(recommendations)
    }
