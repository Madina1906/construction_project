from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, date


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, server_default=func.now())
    due_date = Column(DateTime, nullable=True)  # SQLAlchemy datetime

    task = relationship("Task", back_populates="assignments")
    user = relationship("User", back_populates="assigned_tasks")