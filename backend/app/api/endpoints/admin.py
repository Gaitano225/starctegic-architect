from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.project import Project
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all users (Admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/stats")
def read_stats(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve platform statistics (Admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    
    user_count = db.query(User).count()
    project_count = db.query(Project).count()
    
    return {
        "total_users": user_count,
        "total_projects": project_count,
    }
