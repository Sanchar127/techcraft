from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


# -----------------------
# AUTH SCHEMAS
# -----------------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------
# SCORE SCHEMAS
# -----------------------
class ScoreCreate(BaseModel):
    category: str
    score: int = Field(ge=1, le=5)
    note: Optional[str] = None


# -----------------------
# CANDIDATE SCHEMAS
# -----------------------
class CandidateResponse(BaseModel):
    id: str
    name: str
    email: str
    role_applied: str
    status: str
    skills: List[str]

    internal_notes: Optional[str] = None
    ai_summary: Optional[str] = None