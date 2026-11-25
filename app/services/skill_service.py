from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate


def get_all_skills(db: Session):
    return db.query(Skill).order_by(Skill.level.desc()).all()


def get_skill(db: Session, skill_id: int):
    return db.query(Skill).filter(Skill.id == skill_id).first()


def create_skill(db: Session, data: SkillCreate) -> Skill:
    skill = Skill(**data.model_dump())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill) -> None:
    db.delete(skill)
    db.commit()