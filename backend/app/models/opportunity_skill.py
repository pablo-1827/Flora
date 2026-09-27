from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class OpportunitySkill(Base):
    __tablename__ = "opportunity_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    opportunity: Mapped["Opportunity"] = relationship(back_populates="skill_links")
    skill: Mapped["Skill"] = relationship(back_populates="opportunity_links")

    __table_args__ = (
        Index("ix_opportunity_skills_opportunity_skill", "opportunity_id", "skill_id", unique=True),
    )
