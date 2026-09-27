from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.category import Category
from app.models.interest import Interest
from app.models.skill import Skill
from app.models.student_category import StudentCategory
from app.models.student_interest import StudentInterest
from app.models.student_profile import StudentProfile
from app.models.student_skill import StudentSkill
from app.models.user import User
from app.schemas.student_profile import StudentProfilePayload, StudentProfileResponse

router = APIRouter(prefix="/profile", tags=["Student Profile"])


def _normalize_catalog_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values or []:
        text = " ".join(str(value).split())
        if not text:
            continue
        key = text.lower()
        if key not in seen:
            seen.add(key)
            normalized.append(text)
    return sorted(normalized, key=lambda item: item.lower())


def _get_or_create_catalog_item(db: Session, model, name: str):
    cleaned = " ".join(str(name).split())
    if not cleaned:
        raise ValueError("Catalog item cannot be empty.")
    item = db.query(model).filter(func.lower(model.name) == cleaned.lower()).first()
    if item is None:
        item = model(name=cleaned)
        db.add(item)
        db.flush()
    return item


def _build_profile_payload(profile: StudentProfile, current_user: User) -> StudentProfileResponse:
    return StudentProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        email=current_user.email,
        full_name=profile.full_name,
        college=profile.college,
        degree=profile.degree,
        branch=profile.branch,
        current_academic_year=profile.current_academic_year,
        graduation_year=profile.graduation_year,
        skills=_normalize_catalog_values([link.skill.name for link in profile.skills]),
        interests=_normalize_catalog_values([link.interest.name for link in profile.interests]),
        categories=_normalize_catalog_values([link.category.name for link in profile.categories]),
        preferred_mode=profile.preferred_mode,
        preferred_location=profile.preferred_location,
        resume_url=profile.resume_url,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


def _apply_catalog_links(profile: StudentProfile, db: Session, payload: StudentProfilePayload):
    profile.skills = []
    for name in _normalize_catalog_values(payload.skills):
        skill = _get_or_create_catalog_item(db, Skill, name)
        profile.skills.append(StudentSkill(skill_id=skill.id))

    profile.interests = []
    for name in _normalize_catalog_values(payload.interests):
        interest = _get_or_create_catalog_item(db, Interest, name)
        profile.interests.append(StudentInterest(interest_id=interest.id))

    profile.categories = []
    for name in _normalize_catalog_values(payload.categories):
        category = _get_or_create_catalog_item(db, Category, name)
        profile.categories.append(StudentCategory(category_id=category.id))


@router.get("", response_model=StudentProfileResponse)
def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found.")
    return _build_profile_payload(profile, current_user)


@router.post("", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(payload: StudentProfilePayload, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if existing_profile is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student profile already exists.")

    profile = StudentProfile(
        user_id=current_user.id,
        full_name=payload.full_name,
        college=payload.college,
        degree=payload.degree,
        branch=payload.branch,
        current_academic_year=payload.current_academic_year,
        graduation_year=payload.graduation_year,
        preferred_mode=payload.preferred_mode,
        preferred_location=payload.preferred_location,
        resume_url=payload.resume_url,
    )
    db.add(profile)
    db.flush()
    _apply_catalog_links(profile, db, payload)
    db.commit()
    db.refresh(profile)
    return _build_profile_payload(profile, current_user)


@router.put("", response_model=StudentProfileResponse)
def update_profile(payload: StudentProfilePayload, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found.")

    profile.full_name = payload.full_name
    profile.college = payload.college
    profile.degree = payload.degree
    profile.branch = payload.branch
    profile.current_academic_year = payload.current_academic_year
    profile.graduation_year = payload.graduation_year
    profile.preferred_mode = payload.preferred_mode
    profile.preferred_location = payload.preferred_location
    profile.resume_url = payload.resume_url

    _apply_catalog_links(profile, db, payload)
    db.commit()
    db.refresh(profile)
    return _build_profile_payload(profile, current_user)
