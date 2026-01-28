from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
# from app.models.user import User  # Supprimé pour éviter import circulaire
from app.models.project import Project as ProjectModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve user projects.
    """
    projects = db.query(ProjectModel).filter(ProjectModel.user_id == current_user.id).offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: ProjectCreate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new project.
    """
    project = ProjectModel(
        **project_in.dict(),
        user_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/{id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get project by ID.
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == id, ProjectModel.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    project_in: ProjectUpdate,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a project.
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == id, ProjectModel.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(project, field, update_data[field])
    
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{id}", response_model=Project)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a project.
    """
    project = db.query(ProjectModel).filter(ProjectModel.id == id, ProjectModel.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return project
