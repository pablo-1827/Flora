"""phase2 schema

Revision ID: a8f714d6f8b1
Revises: 
Create Date: 2026-09-27 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a8f714d6f8b1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "student_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("college", sa.String(length=255), nullable=False),
        sa.Column("degree", sa.String(length=100), nullable=False),
        sa.Column("branch", sa.String(length=100), nullable=False),
        sa.Column("current_academic_year", sa.String(length=50), nullable=False),
        sa.Column("graduation_year", sa.Integer(), nullable=False),
        sa.Column("preferred_mode", sa.String(length=20), nullable=False),
        sa.Column("preferred_location", sa.String(length=255), nullable=True),
        sa.Column("resume_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_student_profiles_college_degree", "student_profiles", ["college", "degree"], unique=False)

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_skills_name"), "skills", ["name"], unique=True)

    op.create_table(
        "student_skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_profile_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["student_profile_id"], ["student_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_profile_id", "skill_id"),
    )
    op.create_index("ix_student_skills_profile_skill", "student_skills", ["student_profile_id", "skill_id"], unique=True)

    op.create_table(
        "interests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_interests_name"), "interests", ["name"], unique=True)

    op.create_table(
        "student_interests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_profile_id", sa.Integer(), nullable=False),
        sa.Column("interest_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["student_profile_id"], ["student_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["interest_id"], ["interests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_profile_id", "interest_id"),
    )
    op.create_index("ix_student_interests_profile_interest", "student_interests", ["student_profile_id", "interest_id"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)

    op.create_table(
        "student_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_profile_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["student_profile_id"], ["student_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_profile_id", "category_id"),
    )
    op.create_index("ix_student_categories_profile_category", "student_categories", ["student_profile_id", "category_id"], unique=True)

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sources_name"), "sources", ["name"], unique=False)

    op.create_table(
        "opportunities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("organization", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("skills_text", sa.Text(), nullable=True),
        sa.Column("eligibility_text", sa.Text(), nullable=True),
        sa.Column("eligible_degrees", sa.String(length=255), nullable=True),
        sa.Column("eligible_branches", sa.String(length=255), nullable=True),
        sa.Column("eligible_years", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("mode", sa.String(length=30), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("benefits", sa.Text(), nullable=True),
        sa.Column("application_url", sa.String(length=500), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "published", "expired", "archived", name="opportunity_status"),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_opportunities_status_deadline", "opportunities", ["status", "deadline"], unique=False)
    op.create_index("ix_opportunities_category_status", "opportunities", ["category_id", "status"], unique=False)
    op.create_index(op.f("ix_opportunities_title"), "opportunities", ["title"], unique=False)

    op.create_table(
        "opportunity_skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("opportunity_id", "skill_id"),
    )
    op.create_index("ix_opportunity_skills_opportunity_skill", "opportunity_skills", ["opportunity_id", "skill_id"], unique=True)

    op.create_table(
        "opportunity_eligibility",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("eligible_degrees", sa.String(length=255), nullable=True),
        sa.Column("eligible_branches", sa.String(length=255), nullable=True),
        sa.Column("eligible_years", sa.String(length=255), nullable=True),
        sa.Column("min_academic_year", sa.Integer(), nullable=True),
        sa.Column("max_academic_year", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("opportunity_id"),
    )

    op.create_table(
        "bookmarks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_profile_id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["student_profile_id"], ["student_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_profile_id", "opportunity_id"),
    )
    op.create_index("ix_bookmarks_profile_opportunity", "bookmarks", ["student_profile_id", "opportunity_id"], unique=True)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_profile_id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "interested",
                "planning_to_apply",
                "applied",
                "shortlisted",
                "selected",
                "rejected",
                "withdrawn",
                name="application_status",
            ),
            nullable=False,
            server_default="interested",
        ),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["student_profile_id"], ["student_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_profile_id", "opportunity_id"),
    )
    op.create_index("ix_applications_profile_opportunity", "applications", ["student_profile_id", "opportunity_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_applications_profile_opportunity", table_name="applications")
    op.drop_table("applications")
    op.drop_index("ix_bookmarks_profile_opportunity", table_name="bookmarks")
    op.drop_table("bookmarks")
    op.drop_table("opportunity_eligibility")
    op.drop_index("ix_opportunity_skills_opportunity_skill", table_name="opportunity_skills")
    op.drop_table("opportunity_skills")
    op.drop_index("ix_opportunities_title", table_name="opportunities")
    op.drop_index("ix_opportunities_category_status", table_name="opportunities")
    op.drop_index("ix_opportunities_status_deadline", table_name="opportunities")
    op.drop_table("opportunities")
    op.drop_index(op.f("ix_sources_name"), table_name="sources")
    op.drop_table("sources")
    op.drop_index("ix_student_categories_profile_category", table_name="student_categories")
    op.drop_table("student_categories")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_table("categories")
    op.drop_index("ix_student_interests_profile_interest", table_name="student_interests")
    op.drop_table("student_interests")
    op.drop_index(op.f("ix_interests_name"), table_name="interests")
    op.drop_table("interests")
    op.drop_index("ix_student_skills_profile_skill", table_name="student_skills")
    op.drop_table("student_skills")
    op.drop_index(op.f("ix_skills_name"), table_name="skills")
    op.drop_table("skills")
    op.drop_index("ix_student_profiles_college_degree", table_name="student_profiles")
    op.drop_table("student_profiles")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
