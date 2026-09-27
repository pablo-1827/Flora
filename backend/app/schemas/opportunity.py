from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OpportunitySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    organization: str
    description: str
    category: str | None = None
    category_id: int | None = None
    location: str | None = None
    mode: str
    deadline: datetime | None = None
    status: str
    application_url: str | None = None
    skills: list[str] = Field(default_factory=list)
    eligibility: str | None = None


class OpportunityDetail(OpportunitySummary):
    start_date: datetime | None = None
    benefits: str | None = None
    eligible_degrees: str | None = None
    eligible_branches: str | None = None
    eligible_years: str | None = None
    source_name: str | None = None
    source_url: str | None = None


class RecommendationItem(BaseModel):
    opportunity: OpportunitySummary
    relevance_score: int
    explanation: str


class BookmarkCreate(BaseModel):
    opportunity_id: int


class BookmarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_profile_id: int
    opportunity_id: int
    created_at: datetime | None = None


class ApplicationCreate(BaseModel):
    opportunity_id: int
    status: str = "Interested"
    note: str | None = None


class ApplicationUpdate(BaseModel):
    status: str
    note: str | None = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_profile_id: int
    opportunity_id: int
    status: str
    note: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
