from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String(255))
    tech_stack = Column(String(255))  # example: "Flutter, Firebase"
    github_link = Column(String(255))
    live_link = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)