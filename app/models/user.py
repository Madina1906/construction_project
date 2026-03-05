from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    INVESTOR = "investor"
    GEN_PODRYADCHIK = "gen_podryadchik"
    SUB_PODRYADCHIK = "sub_podryadchik"
    PRORAB = "prorab"
    ISHCHI = "ishchi"
    QABUL_KOMISSIYASI = "qabul_komissiyasi"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)          # keyin bcrypt bilan
    role = Column(Enum(UserRole), nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Relationships
    assigned_tasks = relationship("Assignment", back_populates="user")
    created_projects = relationship("Project", back_populates="created_by")
    