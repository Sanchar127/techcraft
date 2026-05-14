from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..database import SessionLocal
from ..models import User
from ..utils.security import hash_password, verify_password, create_token
from ..schemas import UserCreate, UserLogin, TokenResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# REGISTER
# -----------------------
@router.post("/register", response_model=TokenResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        id=str(uuid.uuid4()),
        email=payload.email,
        password=hash_password(payload.password),
        role="reviewer"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({
        "sub": user.id,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}


# -----------------------
# LOGIN
# -----------------------
@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user.id,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}