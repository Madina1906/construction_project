from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import templates
from app.database import get_db
from app.models.user import User
from app.dependencies import create_session_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login_post(
    response: Response,
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or password != user.password_hash:
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "Username yoki parol noto'g'ri"
            }
        )

    # Token yaratish va cookie ga yozish
    token = create_session_token(user.id)

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        max_age=604800,          # 7 kun
        secure=False,            # localda HTTPS yo'q → False
        samesite="lax"
    )

    # Debug: terminalda ko'rish uchun
    print(f"LOGIN SUCCESS → user_id={user.id}, token yaratildi va cookie o'rnatildi")

    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("session_token")
    print("LOGOUT → cookie o'chirildi")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register_post(
    request: Request,
    username: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "Bu username band"
            }
        )

    new_user = User(
        username=username,
        full_name=full_name,
        password_hash=password,  # keyinchalik bcrypt bilan hash qilinadi
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"REGISTER SUCCESS → username={username}, id={new_user.id}")

    return RedirectResponse(url="/auth/login", status_code=303)