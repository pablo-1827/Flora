from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OpportunityStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    EXPIRED = "expired"
    ARCHIVED = "archived"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    skills_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    eligibility_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    eligible_degrees: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eligible_branches: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eligible_years: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mode: Mapped[str] = mapped_column(String(30), nullable=False, default="online")
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    benefits: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[OpportunityStatus] = mapped_column(SAEnum(OpportunityStatus, name="opportunity_status"), nullable=False, default=OpportunityStatus.DRAFT)
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(back_populates="opportunity_links")
    source: Mapped["Source"] = relationship(back_populates="opportunities")
    skill_links: Mapped[list["OpportunitySkill"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")
    eligibility: Mapped["OpportunityEligibility"] = relationship(back_populates="opportunity", cascade="all, delete-orphan")
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_opportunities_status_deadline", "status", "deadline"),
        Index("ix_opportunities_category_status", "category_id", "status"),
        Index("ix_opportunities_title", "title"),
    )
