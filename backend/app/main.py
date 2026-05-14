from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, candidates
import os

Base.metadata.create_all(bind=engine)

ENV = os.getenv("ENV", "dev")

app = FastAPI(
    docs_url="/docs" if ENV != "prod" else None,
    redoc_url="/redoc" if ENV != "prod" else None,
    openapi_url="/openapi.json" if ENV != "prod" else None,
)

# -----------------------
# CORS FIX (IMPORTANT FOR VITE)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# ROUTES
# -----------------------
app.include_router(auth.router, prefix="/auth")
app.include_router(candidates.router, prefix="/candidates")