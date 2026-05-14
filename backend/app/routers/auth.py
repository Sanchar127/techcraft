from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..database import SessionLocal
from ..models import User
from ..utils.security import hash_password, verify_password, create_token
from ..schemas import UserCreate, UserLogin, TokenResponse
from ..utils.logger import logger  

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):

    logger.info(f"Register attempt email={payload.email}")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        logger.warning(f"Register failed - user exists {payload.email}")
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

    logger.info(f"User registered id={user.id}")

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):

    logger.info(f"Login attempt email={payload.email}")

    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        logger.warning(f"Login failed email={payload.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user.id,
        "role": user.role
    })

    logger.info(f"Login success user_id={user.id}")

    return {"access_token": token, "token_type": "bearer"}