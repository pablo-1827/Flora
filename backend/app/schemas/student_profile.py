from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_MODES = {"online", "offline", "hybrid", "any"}


class StudentProfilePayload(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    college: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=100)
    branch: str = Field(..., min_length=1, max_length=100)
    current_academic_year: str = Field(..., min_length=1, max_length=50)
    graduation_year: int = Field(..., ge=1900, le=2100)
    skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    preferred_mode: str = Field(default="any")
    preferred_location: str | None = Field(default=None, max_length=255)
    resume_url: str | None = Field(default=None, max_length=500)

    @field_validator("preferred_mode")
    @classmethod
    def validate_preferred_mode(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in VALID_MODES:
            raise ValueError("Preferred mode must be one of: online, offline, hybrid, or any.")
        return normalized

    @field_validator("full_name", "college", "degree", "branch", "current_academic_year")
    @classmethod
    def normalize_text_fields(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("Field cannot be empty.")
        return normalized

    @field_validator("skills", "interests", "categories")
    @classmethod
    def validate_catalog_items(cls, value: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for item in value or []:
            text = " ".join(str(item).split())
            if not text:
                continue
            key = text.lower()
            if key not in seen:
                seen.add(key)
                normalized.append(text)
        return normalized

    @field_validator("preferred_location", "resume_url")
    @classmethod
    def normalize_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = " ".join(str(value).split())
        return normalized or None


class StudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    email: str
    full_name: str
    college: str
    degree: str
    branch: str
    current_academic_year: str
    graduation_year: int
    skills: list[str]
    interests: list[str]
    categories: list[str]
    preferred_mode: str
    preferred_location: str | None = None
    resume_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
