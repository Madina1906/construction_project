from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str
    password: str = Field(..., min_length=6)
    role: str
    phone: str | None = None
    email: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    phone: str | None
    email: str | None

    class Config:
        from_attributes = True