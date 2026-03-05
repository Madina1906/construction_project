from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app import templates
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.models.task import Task, TaskStatus
from app.models.assignment import Assignment

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Agar user roli ISHCHI bo‘lsa → unga biriktirilgan vazifalarni olamiz
    user_tasks = None
    if current_user.role == UserRole.ISHCHI:
        user_tasks = (
            db.query(Task)
            .join(Assignment)
            .filter(Assignment.user_id == current_user.id)
            .all()
        )

    context = {
        "request": request,
        "title": "Dashboard",
        "user": current_user,
        "projects": [
            {"id": 1, "name": "10 qavatli uy", "progress": 42},
            {"id": 2, "name": "Ofis binosi", "progress": 15},
        ],
        "user_tasks": user_tasks,               # ishchi uchun vazifalar ro‘yxati
        "is_ishchi": current_user.role == UserRole.ISHCHI,
    }

    return templates.TemplateResponse("dashboard.html", context)