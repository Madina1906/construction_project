from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    assigned = "assigned"
    worker_done = "worker_done"
    prorab_done = "prorab_done"
    subcontractor_done = "subcontractor_done"
    gencontractor_done = "gencontractor_done"
    commission_done = "commission_done"

class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id")) 
    old_status = Column(Enum(TaskStatus))
    new_status = Column(Enum(TaskStatus))
    changed_at = Column(DateTime, server_default=func.now())

    task = relationship("Task", back_populates="status_history")
    