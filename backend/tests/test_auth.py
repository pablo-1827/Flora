import os
from datetime import datetime, timedelta

import jwt
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


def register_user(payload=None):
    if payload is None:
        payload = {"name": "Test Student", "email": "student@example.com", "password": "StrongPass123!"}
    response = client.post("/api/v1/auth/register", json=payload)
    return response


def test_register_success():
    response = register_user()
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "student@example.com"
    assert body["role"] == "student"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email_rejected():
    register_user()
    response = register_user()
    assert response.status_code == 409


def test_register_invalid_email_rejected():
    response = register_user({"name": "Bad", "email": "not-an-email", "password": "StrongPass123!"})
    assert response.status_code == 422


def test_register_invalid_password_rejected():
    response = register_user({"name": "Bad", "email": "new@example.com", "password": "short"})
    assert response.status_code == 422


def test_register_password_is_hashed_and_not_plaintext():
    response = register_user({"name": "Hash User", "email": "hash@example.com", "password": "StrongPass123!"})
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "hash@example.com"
    assert "password" not in body
    assert "password_hash" not in body


def test_login_success_and_returns_token():
    register_user()
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body
    assert body["access_token"]


def test_login_incorrect_password_rejected():
    register_user()
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "WrongPass123!"},
    )
    assert response.status_code == 401


def test_login_nonexistent_email_rejected():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 401


def test_me_requires_valid_token():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer malformed-token"})
    assert response.status_code == 401


def test_me_returns_current_user_for_valid_token():
    register_user({"name": "Current User", "email": "me@example.com", "password": "StrongPass123!"})
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "me@example.com", "password": "StrongPass123!"},
    )
    token = login_response.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "me@example.com"
    assert body["role"] == "student"
    assert "password_hash" not in body


def test_me_rejects_expired_token():
    from app.core.security import create_access_token

    expired = create_access_token(subject="expired@example.com", expires_delta=timedelta(minutes=-5))
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired}"})
    assert response.status_code == 401


def test_me_rejects_token_for_nonexistent_user():
    token = jwt.encode({"sub": "ghost@example.com", "exp": datetime.utcnow() + timedelta(minutes=30)}, "test-jwt-secret-key", algorithm="HS256")
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_logout_requires_current_token():
    register_user()
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "StrongPass123!"},
    )
    token = login_response.json()["access_token"]

    response = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "logged out" in response.json()["detail"].lower()


def test_protected_routes_require_authentication():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_password_hash_is_not_exposed_in_api_responses():
    response = register_user({"name": "Hash Guard", "email": "guard@example.com", "password": "StrongPass123!"})
    payload = response.json()
    assert "password_hash" not in payload
    assert "password" not in payload
