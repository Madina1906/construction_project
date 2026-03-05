from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    start_date = Column(DateTime, server_default=func.now())
    planned_end_date = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", back_populates="created_projects")
    tasks = relationship("Task", back_populates="project")