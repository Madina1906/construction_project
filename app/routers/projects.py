from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.project import Project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/")
def create_project(name: str, address: str = None, db: Session = Depends(get_db)):
    project = Project(name=name, address=address)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()