from sqlalchemy import inspect

from app.core.database import Base, engine
from app.models import (
    Application,
    Bookmark,
    Category,
    Interest,
    Opportunity,
    OpportunityEligibility,
    OpportunitySkill,
    Skill,
    Source,
    StudentCategory,
    StudentInterest,
    StudentProfile,
    StudentSkill,
    User,
)


def test_metadata_registers_expected_tables():
    table_names = set(Base.metadata.tables.keys())
    expected = {
        "users",
        "student_profiles",
        "skills",
        "student_skills",
        "interests",
        "student_interests",
        "categories",
        "student_categories",
        "opportunities",
        "opportunity_skills",
        "opportunity_eligibility",
        "bookmarks",
        "applications",
        "sources",
    }
    assert expected.issubset(table_names)


def test_key_constraints_and_relationships_are_present():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "student_profiles" in tables
    assert "opportunities" in tables

    fk_student_profile = inspector.get_foreign_keys("student_profiles")
    assert any(fk["constrained_columns"] == ["user_id"] for fk in fk_student_profile)

    fk_bookmark = inspector.get_foreign_keys("bookmarks")
    assert any(fk["constrained_columns"] == ["student_profile_id"] and fk["referred_table"] == "student_profiles" for fk in fk_bookmark)
    assert any(fk["constrained_columns"] == ["opportunity_id"] and fk["referred_table"] == "opportunities" for fk in fk_bookmark)

    unique_constraints = inspector.get_unique_constraints("student_skills")
    assert any(column["column_names"] == ["student_profile_id", "skill_id"] for column in unique_constraints)

    unique_application = inspector.get_unique_constraints("applications")
    assert any(column["column_names"] == ["student_profile_id", "opportunity_id"] for column in unique_application)


def test_model_imports_and_names():
    assert User.__tablename__ == "users"
    assert StudentProfile.__tablename__ == "student_profiles"
    assert Skill.__tablename__ == "skills"
    assert Opportunity.__tablename__ == "opportunities"
    assert Source.__tablename__ == "sources"
    assert Bookmark.__tablename__ == "bookmarks"
    assert Application.__tablename__ == "applications"


def test_model_relationships_exist():
    assert hasattr(User, "profile")
    assert hasattr(StudentProfile, "skills")
    assert hasattr(StudentProfile, "interests")
    assert hasattr(StudentProfile, "categories")
    assert hasattr(Opportunity, "skill_links")
    assert hasattr(Opportunity, "eligibility")
    assert hasattr(Opportunity, "bookmarks")
    assert hasattr(Opportunity, "applications")
