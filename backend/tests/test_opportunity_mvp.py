import os
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

from app.core.database import Base, engine, get_db
from app.main import app
from app.models.category import Category
from app.models.interest import Interest
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.opportunity_eligibility import OpportunityEligibility
from app.models.opportunity_skill import OpportunitySkill
from app.models.skill import Skill
from app.models.student_category import StudentCategory
from app.models.student_interest import StudentInterest
from app.models.student_profile import StudentProfile
from app.models.student_skill import StudentSkill

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def register_and_login(email="student@example.com", password="StrongPass123!", name="Demo Student"):
    response = client.post(
        "/api/v1/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    assert response.status_code == 201, response.text
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200, login_response.text
    return {"Authorization": f"Bearer {login_response.json()['access_token']}"}


def make_profile_and_opportunities(db_session):
    category = Category(name="Hackathons")
    skill_python = Skill(name="Python")
    skill_fastapi = Skill(name="FastAPI")
    skill_ml = Skill(name="Machine Learning")
    interest_ai = Interest(name="AI")
    interest_startups = Interest(name="Startups")
    db_session.add_all([category, skill_python, skill_fastapi, skill_ml, interest_ai, interest_startups])
    db_session.flush()

    profile = StudentProfile(
        user_id=1,
        full_name="Demo Student",
        college="IIT Delhi",
        degree="B.Tech",
        branch="Computer Science",
        current_academic_year="3rd Year",
        graduation_year=2027,
        preferred_mode="hybrid",
        preferred_location="Bengaluru",
    )
    db_session.add(profile)
    db_session.flush()

    profile.skills = [
        StudentSkill(skill_id=skill_python.id),
        StudentSkill(skill_id=skill_fastapi.id),
        StudentSkill(skill_id=skill_ml.id),
    ]
    profile.interests = [
        StudentInterest(interest_id=interest_ai.id),
        StudentInterest(interest_id=interest_startups.id),
    ]
    profile.categories = [StudentCategory(category_id=category.id)]

    opportunity = Opportunity(
        title="AI Builders Sprint",
        organization="OpenAI for Good",
        description="Build impactful AI prototypes",
        category_id=category.id,
        mode="hybrid",
        location="Bengaluru",
        deadline=datetime.utcnow() + timedelta(days=10),
        status=OpportunityStatus.PUBLISHED,
    )
    db_session.add(opportunity)
    db_session.flush()

    db_session.add_all([
        OpportunitySkill(opportunity_id=opportunity.id, skill_id=skill_python.id),
        OpportunitySkill(opportunity_id=opportunity.id, skill_id=skill_fastapi.id),
        OpportunitySkill(opportunity_id=opportunity.id, skill_id=skill_ml.id),
        OpportunityEligibility(
            opportunity_id=opportunity.id,
            eligible_degrees="B.Tech",
            eligible_branches="Computer Science",
            eligible_years="2nd Year,3rd Year,4th Year",
        ),
    ])
    db_session.commit()
    return profile, opportunity


def test_list_opportunities_supports_search_filters_and_pagination():
    db_session = next(get_db())
    make_profile_and_opportunities(db_session)

    response = client.get("/api/v1/opportunities?search=builders&category=Hackathons&mode=hybrid&location=Bengaluru&limit=10")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["title"] == "AI Builders Sprint"

    response = client.get("/api/v1/opportunities?skip=0&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_recommendations_returns_relevance_score_and_explanation():
    db_session = next(get_db())
    make_profile_and_opportunities(db_session)
    headers = register_and_login(email="recommend@example.com")

    response = client.get("/api/v1/recommendations", headers=headers)
    assert response.status_code == 200, response.text
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["relevance_score"] >= 0
    assert payload[0]["relevance_score"] <= 100
    assert "skills" in payload[0]["explanation"].lower() or "interest" in payload[0]["explanation"].lower()


def test_saved_bookmarks_and_application_status_flow():
    db_session = next(get_db())
    profile, opportunity = make_profile_and_opportunities(db_session)
    headers = register_and_login(email="save@example.com")

    # create profile for the authenticated user
    profile_response = client.post(
        "/api/v1/profile",
        json={
            "full_name": "Save User",
            "college": "IIT Delhi",
            "degree": "B.Tech",
            "branch": "Computer Science",
            "current_academic_year": "3rd Year",
            "graduation_year": 2027,
            "skills": ["Python", "FastAPI"],
            "interests": ["AI"],
            "categories": ["Hackathons"],
            "preferred_mode": "hybrid",
            "preferred_location": "Bengaluru",
        },
        headers=headers,
    )
    assert profile_response.status_code == 201

    bookmark = client.post("/api/v1/saved-opportunities", json={"opportunity_id": opportunity.id}, headers=headers)
    assert bookmark.status_code == 201, bookmark.text

    saved = client.get("/api/v1/saved-opportunities", headers=headers)
    assert saved.status_code == 200
    assert saved.json()[0]["id"] == opportunity.id

    delete_response = client.delete(f"/api/v1/saved-opportunities/{opportunity.id}", headers=headers)
    assert delete_response.status_code == 200

    app_response = client.post(
        "/api/v1/applications",
        json={"opportunity_id": opportunity.id, "status": "Applied", "note": "I am interested"},
        headers=headers,
    )
    assert app_response.status_code == 201, app_response.text
    application_body = app_response.json()
    assert application_body["status"] == "Applied"

    list_apps = client.get("/api/v1/applications", headers=headers)
    assert list_apps.status_code == 200
    assert list_apps.json()[0]["status"] == "Applied"

    update_response = client.put(
        f"/api/v1/applications/{opportunity.id}",
        json={"status": "Shortlisted", "note": "Strong fit"},
        headers=headers,
    )
    assert update_response.status_code == 200, update_response.text
    assert update_response.json()["status"] == "Shortlisted"
