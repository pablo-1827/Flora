from app.models.application import Application
from app.models.bookmark import Bookmark
from app.models.category import Category
from app.models.interest import Interest
from app.models.opportunity import Opportunity
from app.models.opportunity_eligibility import OpportunityEligibility
from app.models.opportunity_skill import OpportunitySkill
from app.models.skill import Skill
from app.models.source import Source
from app.models.student_category import StudentCategory
from app.models.student_interest import StudentInterest
from app.models.student_profile import StudentProfile
from app.models.student_skill import StudentSkill
from app.models.user import User
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

__all__ = [
    "Base",
    "User",
    "StudentProfile",
    "Skill",
    "StudentSkill",
    "Interest",
    "StudentInterest",
    "Category",
    "StudentCategory",
    "Source",
    "Opportunity",
    "OpportunitySkill",
    "OpportunityEligibility",
    "Bookmark",
    "Application",
]
