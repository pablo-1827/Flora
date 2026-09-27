from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OpportunityEligibility(Base):
    __tablename__ = "opportunity_eligibility"

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id", ondelete="CASCADE"), unique=True, nullable=False)
    eligible_degrees: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eligible_branches: Mapped[str | None] = mapped_column(String(255), nullable=True)
    eligible_years: Mapped[str | None] = mapped_column(String(255), nullable=True)
    min_academic_year: Mapped[int | None] = mapped_column(nullable=True)
    max_academic_year: Mapped[int | None] = mapped_column(nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    opportunity: Mapped["Opportunity"] = relationship(back_populates="eligibility")
