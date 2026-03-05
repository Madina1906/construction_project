from sqlalchemy import Column, Integer, String, ForeignKey, Enum
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


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.assigned)
    description = Column(String, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")

    assignments = relationship(
        "Assignment",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    status_history = relationship(
        "StatusHistory",
        back_populates="task",
        cascade="all, delete-orphan"
    )



