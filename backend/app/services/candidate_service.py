from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Candidate, Score
import uuid


def get_candidates(db: Session, skip=0, limit=20, status=None, role=None, keyword=None):

    query = db.query(Candidate).filter(Candidate.deleted_at == None)

    if status:
        query = query.filter(Candidate.status == status)

    if role:
        query = query.filter(Candidate.role_applied == role)

    if keyword:
        query = query.filter(Candidate.name.contains(keyword))

    return query.offset(skip).limit(limit).all()