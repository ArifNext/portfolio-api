from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.schemas.skill import SkillCreate, SkillOut
from app.services import skill_service

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("", response_model=List[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return skill_service.get_all_skills(db)


@router.post("", response_model=SkillOut, status_code=201, dependencies=[Depends(require_admin)])
def add_skill(data: SkillCreate, db: Session = Depends(get_db)):
    return skill_service.create_skill(db, data)


@router.delete("/{skill_id}", status_code=204, dependencies=[Depends(require_admin)])
def remove_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = skill_service.get_skill(db, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_service.delete_skill(db, skill)