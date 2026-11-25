from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    level = Column(Integer, default=50)  # 0 to 100
    icon = Column(String(255))