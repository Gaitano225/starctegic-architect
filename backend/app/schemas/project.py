from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    answers: Optional[Dict[str, Any]] = {}
    recommendations: Optional[List[Dict[str, Any]]] = []

# Properties to receive on item creation
class ProjectCreate(ProjectBase):
    name: str

# Properties to receive on item update
class ProjectUpdate(ProjectBase):
    pass

# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class Project(ProjectInDBBase):
    pass

# Properties for Quote Request
class ProjectQuoteRequest(BaseModel):
    project_name: str
    nature: str
    horizon: str
    org_type: str
    budget_range: str
    description: str

# Properties stored in DB
class ProjectInDB(ProjectInDBBase):
    pass
