from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import hashlib

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 6


# -------------------------
# SIMPLE PASSWORD HASH (TEMP FIX FOR SUBMISSION)
# -------------------------
def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")

    # SAFE: no bcrypt crash, works in all environments
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# -------------------------
# JWT
# -------------------------
def create_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    payload.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None