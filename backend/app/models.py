from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from datetime import datetime
from .database import Base


# -----------------------
# USER TABLE (NEW)
# -----------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # IMPORTANT: role-based access control
    role = Column(String, default="reviewer", index=True)
    # values: "admin" | "reviewer"

    created_at = Column(DateTime, default=datetime.utcnow)


# -----------------------
# CANDIDATE TABLE
# -----------------------
class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

    role_applied = Column(String, index=True)
    status = Column(String, index=True, default="new")

    skills = Column(JSON)

    internal_notes = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # soft delete (IMPORTANT requirement)
    deleted_at = Column(DateTime, nullable=True)


# -----------------------
# SCORE TABLE
# -----------------------
class Score(Base):
    __tablename__ = "scores"

    id = Column(String, primary_key=True)

    candidate_id = Column(String, ForeignKey("candidates.id"), index=True)

    # FK to users table (IMPORTANT improvement)
    reviewer_id = Column(String, ForeignKey("users.id"), index=True)

    category = Column(String)
    score = Column(Integer)
    note = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)