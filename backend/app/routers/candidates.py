from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import asyncio
from datetime import datetime

from ..database import SessionLocal
from ..models import Candidate, Score
from ..services.candidate_service import get_candidates
from ..deps import get_current_user, require_role
from ..utils.logger import logger 

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_candidates(
    skip: int = 0,
    limit: int = 20,
    status: str = None,
    role: str = None,
    keyword: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    logger.info(f"List candidates called by user={user['sub']} skip={skip} limit={limit}")

    limit = min(limit, 50)

    query = db.query(Candidate).filter(Candidate.deleted_at == None)

    if status:
        query = query.filter(Candidate.status == status)

    if role:
        query = query.filter(Candidate.role_applied == role)

    if keyword:
        query = query.filter(Candidate.name.ilike(f"%{keyword}%"))

    total = query.count()
    candidates = query.offset(skip).limit(limit).all()

    logger.info(f"Candidates fetched: total={total} returned={len(candidates)}")

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": candidates
    }


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    logger.info(f"Get candidate {candidate_id} by user={user['sub']}")

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        logger.warning(f"Candidate not found: {candidate_id}")
        raise HTTPException(status_code=404, detail="Candidate not found")

    if user["role"] != "admin":
        candidate.internal_notes = None

    return candidate


@router.post("/")
def create_candidate(
    name: str,
    email: str,
    role_applied: str,
    skills: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    logger.info(f"Admin {user['sub']} creating candidate {email}")

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

    logger.info(f"Candidate created id={candidate.id}")

    return candidate
@router.put("/{candidate_id}")
def update_candidate(
    candidate_id: str,
    name: str = None,
    role_applied: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    if name:
        candidate.name = name
    if role_applied:
        candidate.role_applied = role_applied
    if status:
        candidate.status = status

    db.commit()
    db.refresh(candidate)

    return candidate

@router.post("/{candidate_id}/scores")
def add_score(
    candidate_id: str,
    category: str,
    score: int,
    note: str = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(f"Score attempt candidate={candidate_id} by reviewer={user['sub']} score={score}")

    if score < 1 or score > 5:
        logger.warning("Invalid score submitted")
        raise HTTPException(status_code=400, detail="Score must be 1-5")

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        logger.warning(f"Score failed - candidate not found {candidate_id}")
        raise HTTPException(status_code=404, detail="Candidate not found")

    new_score = Score(
        id=str(uuid.uuid4()),
        candidate_id=candidate_id,
        reviewer_id=user["sub"],
        category=category,
        score=score,
        note=note
    )

    db.add(new_score)
    db.commit()

    logger.info(f"Score saved for candidate={candidate_id}")

    return {"message": "Score submitted successfully"}


@router.post("/{candidate_id}/summary")
async def generate_summary(candidate_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    logger.info(f"AI summary requested for {candidate_id}")

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.deleted_at == None
    ).first()

    if not candidate:
        logger.warning(f"Summary failed candidate not found {candidate_id}")
        raise HTTPException(status_code=404, detail="Candidate not found")

    await asyncio.sleep(2)

    candidate.ai_summary = f"AI-generated summary for {candidate.name}"
    db.commit()

    logger.info(f"Summary generated for {candidate_id}")

    return {"summary": candidate.ai_summary}


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: str, user=Depends(require_role("admin")), db: Session = Depends(get_db)):

    logger.info(f"Admin delete request candidate={candidate_id}")

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        logger.warning(f"Delete failed candidate not found {candidate_id}")
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.deleted_at = datetime.utcnow()
    candidate.status = "archived"

    db.commit()

    logger.info(f"Candidate soft deleted {candidate_id}")

    return {"message": "Candidate soft deleted"}