from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_profile_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student_profile: Mapped["StudentProfile"] = relationship(back_populates="bookmarks")
    opportunity: Mapped["Opportunity"] = relationship(back_populates="bookmarks")

    __table_args__ = (
        Index("ix_bookmarks_profile_opportunity", "student_profile_id", "opportunity_id", unique=True),
    )
