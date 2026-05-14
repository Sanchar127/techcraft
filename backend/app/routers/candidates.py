from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import asyncio
from datetime import datetime

from ..database import SessionLocal
from ..models import Candidate, Score
from ..services.candidate_service import get_candidates
from ..deps import get_current_user, require_role

router = APIRouter()


# -----------------------
# DB DEPENDENCY
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# GET ALL CANDIDATES
# -----------------------
@router.get("/")
def list_candidates(
    skip: int = 0,
    limit: int = 20,
    status: str = None,
    role: str = None,
    keyword: str = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    limit = min(limit, 50)

    return get_candidates(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        role=role,
        keyword=keyword
    )


# -----------------------
# GET SINGLE CANDIDATE
# -----------------------
@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # 🔐 ROLE-BASED FIELD HIDING
    if user["role"] != "admin":
        candidate.internal_notes = None

    return candidate

@router.post("/")
def create_candidate(
    name: str,
    email: str,
    role_applied: str,
    skills: str,  # keep simple for now: comma-separated string
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    candidate = Candidate(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        role_applied=role_applied,
        skills=skills.split(","),
        status="new",
        deleted_at=None
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate
# -----------------------
# ADD SCORE
# -----------------------
@router.post("/{candidate_id}/scores")
def add_score(
    candidate_id: str,
    category: str,
    score: int,
    note: str = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if score < 1 or score > 5:
        raise HTTPException(status_code=400, detail="Score must be 1-5")

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    new_score = Score(
        id=str(uuid.uuid4()),
        candidate_id=candidate_id,
        reviewer_id=user["sub"],   # user.id from JWT
        category=category,
        score=score,
        note=note
    )

    db.add(new_score)
    db.commit()

    return {"message": "Score submitted successfully"}


# -----------------------
# AI SUMMARY (mock async)
# -----------------------
@router.post("/{candidate_id}/summary")
async def generate_summary(
    candidate_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # simulate LLM delay
    await asyncio.sleep(2)

    candidate.ai_summary = f"AI-generated summary for {candidate.name}"
    db.commit()

    return {"summary": candidate.ai_summary}


# -----------------------
# SOFT DELETE CANDIDATE
# -----------------------
@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: str,
    user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.deleted_at = datetime.utcnow()
    candidate.status = "archived"

    db.commit()

    return {"message": "Candidate soft deleted"}