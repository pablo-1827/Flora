from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StudentCategory(Base):
    __tablename__ = "student_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_profile_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student_profile: Mapped["StudentProfile"] = relationship(back_populates="categories")
    category: Mapped["Category"] = relationship(back_populates="student_links")

    __table_args__ = (
        Index("ix_student_categories_profile_category", "student_profile_id", "category_id", unique=True),
    )
