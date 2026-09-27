from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    college: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)
    current_academic_year: Mapped[str] = mapped_column(String(50), nullable=False)
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    preferred_mode: Mapped[str] = mapped_column(String(20), nullable=False, default="any")
    preferred_location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="profile")
    skills: Mapped[list["StudentSkill"]] = relationship(back_populates="student_profile", cascade="all, delete-orphan")
    interests: Mapped[list["StudentInterest"]] = relationship(back_populates="student_profile", cascade="all, delete-orphan")
    categories: Mapped[list["StudentCategory"]] = relationship(back_populates="student_profile", cascade="all, delete-orphan")
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="student_profile", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="student_profile", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_student_profiles_college_degree", "college", "degree"),
    )
