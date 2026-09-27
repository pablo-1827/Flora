import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

from app.core.database import Base, engine
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def register_and_login(email="student@example.com", password="StrongPass123!", name="Test Student"):
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
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_profile_requires_authentication():
    response = client.get("/api/v1/profile")
    assert response.status_code == 401


def test_student_profile_can_be_created_and_read():
    headers = register_and_login()
    payload = {
        "full_name": "Test Student",
        "college": "IIT Delhi",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "current_academic_year": "3rd Year",
        "graduation_year": 2027,
        "skills": ["Python", "FastAPI", "SQLAlchemy"],
        "interests": ["AI", "Startups"],
        "categories": ["Internships", "Hackathons"],
        "preferred_mode": "hybrid",
        "preferred_location": "Bengaluru",
        "resume_url": "https://example.com/resume.pdf",
    }

    create_response = client.post("/api/v1/profile", json=payload, headers=headers)
    assert create_response.status_code == 201, create_response.text
    body = create_response.json()

    assert body["email"] == "student@example.com"
    assert body["college"] == "IIT Delhi"
    assert body["degree"] == "B.Tech"
    assert body["branch"] == "Computer Science"
    assert body["preferred_mode"] == "hybrid"
    assert body["skills"] == ["FastAPI", "Python", "SQLAlchemy"]
    assert body["interests"] == ["AI", "Startups"]
    assert body["categories"] == ["Hackathons", "Internships"]
    assert body["preferred_location"] == "Bengaluru"
    assert body["resume_url"] == "https://example.com/resume.pdf"

    get_response = client.get("/api/v1/profile", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["full_name"] == "Test Student"


def test_profile_update_replaces_existing_relationships():
    headers = register_and_login(email="update@example.com")
    create_response = client.post(
        "/api/v1/profile",
        json={
            "full_name": "Update Student",
            "college": "NIT Trichy",
            "degree": "B.E.",
            "branch": "Mechanical",
            "current_academic_year": "2nd Year",
            "graduation_year": 2028,
            "skills": ["Python", "Research"],
            "interests": ["Robotics"],
            "categories": ["Scholarships"],
            "preferred_mode": "online",
        },
        headers=headers,
    )
    assert create_response.status_code == 201

    update_response = client.put(
        "/api/v1/profile",
        json={
            "full_name": "Updated Student",
            "college": "NIT Trichy",
            "degree": "B.E.",
            "branch": "Mechanical",
            "current_academic_year": "3rd Year",
            "graduation_year": 2029,
            "skills": ["Python", "ML"],
            "interests": ["AI", "Robotics"],
            "categories": ["Internships"],
            "preferred_mode": "hybrid",
            "preferred_location": "Pune",
            "resume_url": "https://example.com/new-resume.pdf",
        },
        headers=headers,
    )
    assert update_response.status_code == 200, update_response.text
    body = update_response.json()
    assert body["full_name"] == "Updated Student"
    assert body["skills"] == ["ML", "Python"]
    assert body["interests"] == ["AI", "Robotics"]
    assert body["categories"] == ["Internships"]
    assert body["preferred_mode"] == "hybrid"
    assert body["preferred_location"] == "Pune"
    assert body["resume_url"] == "https://example.com/new-resume.pdf"


def test_profile_creation_rejects_duplicate_profile():
    headers = register_and_login(email="dup@example.com")
    profile = {
        "full_name": "Dup Student",
        "college": "VIT Vellore",
        "degree": "B.Tech",
        "branch": "Electronics",
        "current_academic_year": "1st Year",
        "graduation_year": 2028,
        "skills": ["C++"],
        "interests": ["IoT"],
        "categories": ["Hackathons"],
        "preferred_mode": "any",
    }
    first = client.post("/api/v1/profile", json=profile, headers=headers)
    assert first.status_code == 201
    second = client.post("/api/v1/profile", json=profile, headers=headers)
    assert second.status_code == 409


def test_profile_validation_rejects_invalid_mode():
    headers = register_and_login(email="badmode@example.com")
    response = client.post(
        "/api/v1/profile",
        json={
            "full_name": "Bad Mode",
            "college": "Delhi University",
            "degree": "B.A.",
            "branch": "Economics",
            "current_academic_year": "2nd Year",
            "graduation_year": 2027,
            "skills": ["Analytics"],
            "interests": ["Finance"],
            "categories": ["Scholarships"],
            "preferred_mode": "bad-mode",
        },
        headers=headers,
    )
    assert response.status_code == 422
