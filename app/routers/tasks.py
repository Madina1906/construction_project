from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app import templates
from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User, UserRole
from app.models.task import Task, TaskStatus
from app.models.assignment import Assignment
from app.models.project import Project
from app.models.status_history import StatusHistory

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ================= NEW TASK FORM =================
@router.get("/new", response_class=HTMLResponse)
async def new_task_form(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    allowed_roles = [
        UserRole.PRORAB,
        UserRole.SUB_PODRYADCHIK,
        UserRole.GEN_PODRYADCHIK,
        UserRole.ADMIN
    ]

    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Sizda vazifa qo‘shish huquqi yo‘q")

    projects = db.query(Project).all()
    workers = db.query(User).filter(User.role == UserRole.ISHCHI).all()

    return templates.TemplateResponse(
        "tasks/new_task.html",
        {
            "request": request,
            "projects": projects,
            "workers": workers,
            "user": current_user,
        }
    )

# ================= CREATE TASK =================
@router.post("/new")
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    project_id: int = Form(...),
    assigned_to_id: int = Form(...),
    due_date: str = Form(None),  # YYYY-MM-DD format
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    allowed_roles = [
        UserRole.PRORAB,
        UserRole.SUB_PODRYADCHIK,
        UserRole.GEN_PODRYADCHIK,
        UserRole.ADMIN
    ]

    if current_user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Sizda vazifa qo‘shish huquqi yo‘q")

    # ===== CREATE TASK =====
    new_task = Task(
        project_id=project_id,
        title=title,
        description=description,
        status=TaskStatus.assigned
    )
    db.add(new_task)
    db.flush()  # id olish uchun

    # ===== PARSE due_date =====
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="due_date noto‘g‘ri formatda (YYYY-MM-DD)")

    # ===== CREATE ASSIGNMENT =====
    assignment = Assignment(
        task_id=new_task.id,
        user_id=assigned_to_id,
        due_date=due_date_obj
    )
    db.add(assignment)

    db.commit()
    db.refresh(new_task)

    return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)

# ================= MARK TASK DONE =================
@router.post("/{task_id}/done")
def mark_task_done(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status

    if current_user.role == UserRole.ISHCHI:
        task.status = TaskStatus.worker_done
    elif current_user.role == UserRole.PRORAB:
        task.status = TaskStatus.prorab_done
    elif current_user.role == UserRole.SUB_PODRYADCHIK:
        task.status = TaskStatus.subcontractor_done
    elif current_user.role == UserRole.GEN_PODRYADCHIK:
        task.status = TaskStatus.gencontractor_done
    elif current_user.role == UserRole.KOMISSIYA:
        task.status = TaskStatus.commission_done
    else:
        raise HTTPException(status_code=403, detail="Role not allowed")

    history = StatusHistory(
        task_id=task.id,
        user_id=current_user.id,
        old_status=old_status,
        new_status=task.status
    )
    db.add(history)
    db.commit()

    return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)


# ================= GET TASK DETAILS =================
@router.get("/{task_id}", response_class=HTMLResponse)
def task_detail(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task topilmadi")

    return templates.TemplateResponse(
        "tasks/task_detail.html",
        {
            "request": request,
            "task": task,
            "user": current_user
        }
    )