from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
# from app.models.user import User  # Supprimé pour éviter import circulaire
from app.models.project import Project as ProjectModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectQuoteRequest

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
@router.post("/request-quote")
def request_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_in: ProjectQuoteRequest,
    current_user: Any = Depends(deps.get_current_active_user),
) -> Any:
    """
    Request a consultation quote for a project.
    """
    from app.services.notification_service import NotificationService
    
    # Notify Admin (tomgaitano78@mail.com)
    admin_msg = (
        f"NOUVELLE DEMANDE DE DEVIS\n"
        f"------------------------\n"
        f"Client: {current_user.email}\n"
        f"Projet: {quote_in.project_name}\n"
        f"Nature: {quote_in.nature}\n"
        f"Horizon: {quote_in.horizon}\n"
        f"Organisation: {quote_in.org_type}\n"
        f"Budget: {quote_in.budget_range}\n"
        f"Message: {quote_in.description}\n\n"
        f"📧 Répondre à: {current_user.email}\n"
        f"📧 Envoyer à: tomgaitano78@mail.com"
    )
    NotificationService.notify_admin(
        db, 
        "Audit Devis Reçu", 
        admin_msg
    )
    
    # Notify User
    NotificationService.create_notification(
        db,
        current_user.id,
        "Demande de Devis Reçue",
        f"Votre demande de devis pour '{quote_in.project_name}' a été transmise à nos experts. Nous vous répondrons sous 48h à l'adresse {current_user.email}."
    )
    
    return {"message": "Quote request received successfully"}
