from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.database import get_db
from app.models.user import User

# Doimiy kalit (productionda .env dan o'qilishi kerak)
SECRET_KEY = "super_secret_key_change_me_please_2025"
serializer = URLSafeTimedSerializer(SECRET_KEY)


def create_session_token(user_id: int) -> str:
    """User ID dan token yaratadi"""
    return serializer.dumps({"user_id": user_id})


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Cookie dan tokenni o'qib, user ni qaytaradi"""
    token = request.cookies.get("session_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessiya token topilmadi. Iltimos qayta kiring.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        data = serializer.loads(token, max_age=604800)  # 7 kun = 604800 soniya
        user_id: int = data.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token ichida user ID yo'q")
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="Sessiya muddati tugagan")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Token buzilgan yoki noto'g'ri")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    return user