from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.application import Application, ApplicationStatus
from app.models.bookmark import Bookmark
from app.models.category import Category
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.opportunity_eligibility import OpportunityEligibility
from app.models.opportunity_skill import OpportunitySkill
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.schemas.opportunity import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    BookmarkCreate,
    BookmarkResponse,
    OpportunityDetail,
    OpportunitySummary,
    RecommendationItem,
)

router = APIRouter(tags=["Opportunities"])

APPLICATION_STATUS_MAP = {
    "interested": "Interested",
    "planning_to_apply": "Planning to apply",
    "planning to apply": "Planning to apply",
    "applied": "Applied",
    "shortlisted": "Shortlisted",
    "selected": "Selected",
    "rejected": "Rejected",
    "withdrawn": "Withdrawn",
}


def _normalize_status(value: str | ApplicationStatus) -> ApplicationStatus:
    if isinstance(value, ApplicationStatus):
        return value
    cleaned = str(value).strip().lower().replace("-", "_")
    mapping = {
        "interested": ApplicationStatus.INTERESTED,
        "planning_to_apply": ApplicationStatus.PLANNING_TO_APPLY,
        "planning to apply": ApplicationStatus.PLANNING_TO_APPLY,
        "applied": ApplicationStatus.APPLIED,
        "shortlisted": ApplicationStatus.SHORTLISTED,
        "selected": ApplicationStatus.SELECTED,
        "rejected": ApplicationStatus.REJECTED,
        "withdrawn": ApplicationStatus.WITHDRAWN,
    }
    if cleaned not in mapping:
        raise ValueError("Invalid application status.")
    return mapping[cleaned]


def _display_status(value: str | ApplicationStatus | None) -> str:
    if value is None:
        return "Interested"
    if isinstance(value, ApplicationStatus):
        return APPLICATION_STATUS_MAP[value.value]
    return APPLICATION_STATUS_MAP.get(str(value).strip().lower().replace("-", "_"), str(value))


def _serialize_opportunity(opportunity: Opportunity) -> OpportunitySummary:
    category_name = opportunity.category.name if opportunity.category else None
    return OpportunitySummary(
        id=opportunity.id,
        title=opportunity.title,
        organization=opportunity.organization,
        description=opportunity.description,
        category=category_name,
        category_id=opportunity.category_id,
        location=opportunity.location,
        mode=opportunity.mode,
        deadline=opportunity.deadline,
        status=opportunity.status.value,
        application_url=opportunity.application_url,
        skills=[link.skill.name for link in sorted(opportunity.skill_links, key=lambda item: item.skill.name.lower())],
        eligibility=(
            opportunity.eligibility.notes
            if opportunity.eligibility and opportunity.eligibility.notes
            else (
                f"Degrees: {opportunity.eligible_degrees or 'Any'}; Branches: {opportunity.eligible_branches or 'Any'}; Years: {opportunity.eligible_years or 'Any'}"
            )
        ),
    )


def _serialize_opportunity_detail(opportunity: Opportunity) -> OpportunityDetail:
    summary = _serialize_opportunity(opportunity)
    detail = OpportunityDetail(**summary.model_dump())
    detail.start_date = opportunity.start_date
    detail.benefits = opportunity.benefits
    detail.eligible_degrees = opportunity.eligible_degrees
    detail.eligible_branches = opportunity.eligible_branches
    detail.eligible_years = opportunity.eligible_years
    detail.source_name = opportunity.source.name if opportunity.source else None
    detail.source_url = opportunity.source.url if opportunity.source else None
    return detail


def _get_student_profile_for_user(db: Session, current_user: User) -> StudentProfile:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found. Complete your profile before using recommendations or saved items.")
    return profile


def _matches_keyword(text: str | None, value: str) -> bool:
    if not text or not value:
        return False
    return value.lower() in text.lower()


def _normalize_collection(values: list[str] | None) -> set[str]:
    items = set()
    for value in values or []:
        cleaned = " ".join(str(value).split()).lower()
        if cleaned:
            items.add(cleaned)
    return items


def _build_recommendation_explanation(match_parts: list[str]) -> str:
    return "; ".join(match_parts) if match_parts else "No strong matches yet; this opportunity is a general fit."


def _get_opportunity_eligibility_ratio(profile: StudentProfile, opportunity: Opportunity) -> float:
    degree_match = bool(profile.degree and opportunity.eligible_degrees and profile.degree.lower() in opportunity.eligible_degrees.lower())
    branch_match = bool(profile.branch and opportunity.eligible_branches and profile.branch.lower() in opportunity.eligible_branches.lower())
    year_label = str(profile.current_academic_year).lower()
    year_match = bool(opportunity.eligible_years and year_label in opportunity.eligible_years.lower())
    if not opportunity.eligible_degrees and not opportunity.eligible_branches and not opportunity.eligible_years:
        return 1.0
    matches = sum([degree_match, branch_match, year_match])
    return min(1.0, matches / 3.0)


@router.get("/opportunities", response_model=list[OpportunitySummary])
def list_opportunities(
    search: str | None = None,
    category: str | None = None,
    mode: str | None = None,
    location: str | None = None,
    deadline: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    query = db.query(Opportunity).join(Category, Opportunity.category_id == Category.id, isouter=True)

    if search:
        q = f"%{search.strip()}%"
        query = query.filter(or_(Opportunity.title.ilike(q), Opportunity.organization.ilike(q)))
    if category:
        query = query.filter(Category.name.ilike(f"%{category.strip()}%"))
    if mode:
        query = query.filter(Opportunity.mode.ilike(mode.strip()))
    if location:
        query = query.filter(Opportunity.location.ilike(f"%{location.strip()}%"))
    if deadline == "upcoming":
        query = query.filter(Opportunity.deadline.isnot(None)).filter(Opportunity.deadline >= datetime.now(timezone.utc))
    elif deadline == "expired":
        query = query.filter(Opportunity.deadline.isnot(None)).filter(Opportunity.deadline < datetime.now(timezone.utc))

    query = query.filter(Opportunity.status == OpportunityStatus.PUBLISHED)
    query = query.order_by(Opportunity.deadline.asc().nullslast(), Opportunity.created_at.desc())
    opportunities = query.offset(skip).limit(limit).all()
    return [_serialize_opportunity(item) for item in opportunities]


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityDetail)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity is None or opportunity.status != OpportunityStatus.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found.")
    return _serialize_opportunity_detail(opportunity)


@router.get("/recommendations", response_model=list[RecommendationItem])
def get_recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    profile_skills = _normalize_collection([link.skill.name for link in profile.skills])
    profile_interests = _normalize_collection([link.interest.name for link in profile.interests])
    profile_categories = _normalize_collection([link.category.name for link in profile.categories])
    profile_mode = (profile.preferred_mode or "any").strip().lower()
    profile_location = (profile.preferred_location or "").strip().lower()

    opportunities = db.query(Opportunity).filter(Opportunity.status == OpportunityStatus.PUBLISHED).all()
    scored: list[dict[str, Any]] = []

    for opportunity in opportunities:
        opportunity_skills = _normalize_collection([link.skill.name for link in opportunity.skill_links])
        opportunity_category = (opportunity.category.name if opportunity.category else "").lower()
        interest_hits = []
        for interest in profile_interests:
            if interest in opportunity.title.lower() or interest in (opportunity.description or "").lower() or interest in opportunity_category:
                interest_hits.append(interest)

        skill_overlap = sorted(profile_skills & opportunity_skills)
        interest_overlap = sorted(set(interest_hits))
        category_match = 1.0 if opportunity_category and opportunity_category in profile_categories else 0.0
        eligibility_ratio = _get_opportunity_eligibility_ratio(profile, opportunity)

        location_score = 1.0
        if profile_location:
            opp_location = (opportunity.location or "").lower()
            location_score = 1.0 if profile_location in opp_location or opp_location in profile_location else 0.0
        elif profile_location == "":
            location_score = 1.0

        mode_score = 1.0 if profile_mode == "any" or profile_mode == (opportunity.mode or "").lower() else 0.0
        if profile_mode == "hybrid" and (opportunity.mode or "").lower() in {"online", "offline", "hybrid"}:
            mode_score = 1.0

        skill_ratio = len(skill_overlap) / len(profile_skills) if profile_skills else 0.0
        interest_ratio = len(interest_overlap) / len(profile_interests) if profile_interests else 0.0

        score = round(
            (skill_ratio * 30)
            + (interest_ratio * 25)
            + (category_match * 20)
            + (eligibility_ratio * 15)
            + ((location_score * 0.5 + mode_score * 0.5) * 10)
        )

        explanation_parts = []
        if skill_overlap:
            explanation_parts.append(f"Matched skills: {', '.join(skill_overlap[:3])}")
        if interest_overlap:
            explanation_parts.append(f"Matched interests: {', '.join(interest_overlap[:3])}")
        if category_match:
            explanation_parts.append(f"Preferred category: {opportunity.category.name}")
        if eligibility_ratio > 0:
            explanation_parts.append("Education fit matches your degree and year profile")
        if location_score == 1.0 or mode_score == 1.0:
            explanation_parts.append("Location and mode preference align with your profile")

        scored.append(
            {
                "opportunity": _serialize_opportunity(opportunity),
                "relevance_score": max(0, min(100, score)),
                "explanation": _build_recommendation_explanation(explanation_parts),
            }
        )

    scored.sort(key=lambda item: (-item["relevance_score"], item["opportunity"].title.lower()))
    return [RecommendationItem(**payload) for payload in scored[:10]]


@router.post("/saved-opportunities", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def save_opportunity(payload: BookmarkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    opportunity = db.query(Opportunity).filter(Opportunity.id == payload.opportunity_id).first()
    if opportunity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found.")

    existing = db.query(Bookmark).filter(Bookmark.student_profile_id == profile.id, Bookmark.opportunity_id == opportunity.id).first()
    if existing is not None:
        return existing

    bookmark = Bookmark(student_profile_id=profile.id, opportunity_id=opportunity.id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


@router.get("/saved-opportunities", response_model=list[OpportunitySummary])
def list_saved_opportunities(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    opportunities = (
        db.query(Opportunity)
        .join(Bookmark, Bookmark.opportunity_id == Opportunity.id)
        .filter(Bookmark.student_profile_id == profile.id)
        .order_by(Bookmark.created_at.desc())
        .all()
    )
    return [_serialize_opportunity(opportunity) for opportunity in opportunities]


@router.delete("/saved-opportunities/{opportunity_id}")
def delete_saved_opportunity(opportunity_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.student_profile_id == profile.id, Bookmark.opportunity_id == opportunity_id)
        .first()
    )
    if bookmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found.")
    db.delete(bookmark)
    db.commit()
    return {"detail": "Bookmark removed successfully."}


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    opportunity = db.query(Opportunity).filter(Opportunity.id == payload.opportunity_id).first()
    if opportunity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found.")

    try:
        status_value = _normalize_status(payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    existing = (
        db.query(Application)
        .filter(Application.student_profile_id == profile.id, Application.opportunity_id == opportunity.id)
        .first()
    )
    if existing is not None:
        existing.status = status_value
        existing.note = payload.note or existing.note
        existing.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return ApplicationResponse(
            id=existing.id,
            student_profile_id=existing.student_profile_id,
            opportunity_id=existing.opportunity_id,
            status=_display_status(existing.status),
            note=existing.note,
            created_at=existing.created_at,
            updated_at=existing.updated_at,
        )

    application = Application(
        student_profile_id=profile.id,
        opportunity_id=opportunity.id,
        status=status_value,
        note=payload.note,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return ApplicationResponse(
        id=application.id,
        student_profile_id=application.student_profile_id,
        opportunity_id=application.opportunity_id,
        status=_display_status(application.status),
        note=application.note,
        created_at=application.created_at,
        updated_at=application.updated_at,
    )


@router.get("/applications", response_model=list[ApplicationResponse])
def list_applications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = _get_student_profile_for_user(db, current_user)
    applications = (
        db.query(Application)
        .filter(Application.student_profile_id == profile.id)
        .order_by(Application.updated_at.desc())
        .all()
    )
    return [
        ApplicationResponse(
            id=item.id,
            student_profile_id=item.student_profile_id,
            opportunity_id=item.opportunity_id,
            status=_display_status(item.status),
            note=item.note,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in applications
    ]


@router.put("/applications/{opportunity_id}", response_model=ApplicationResponse)
def update_application(
    opportunity_id: int,
    payload: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = _get_student_profile_for_user(db, current_user)
    try:
        status_value = _normalize_status(payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    application = (
        db.query(Application)
        .filter(Application.student_profile_id == profile.id, Application.opportunity_id == opportunity_id)
        .first()
    )
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    application.status = status_value
    application.note = payload.note if payload.note is not None else application.note
    application.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(application)
    return ApplicationResponse(
        id=application.id,
        student_profile_id=application.student_profile_id,
        opportunity_id=application.opportunity_id,
        status=_display_status(application.status),
        note=application.note,
        created_at=application.created_at,
        updated_at=application.updated_at,
    )
