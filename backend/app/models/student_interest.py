from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StudentInterest(Base):
    __tablename__ = "student_interests"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_profile_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    interest_id: Mapped[int] = mapped_column(ForeignKey("interests.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student_profile: Mapped["StudentProfile"] = relationship(back_populates="interests")
    interest: Mapped["Interest"] = relationship(back_populates="student_links")

    __table_args__ = (
        Index("ix_student_interests_profile_interest", "student_profile_id", "interest_id", unique=True),
    )
