from fastapi import FastAPI
# from app.database import Base, engine
# from app.routers import auth, candidates

# Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(auth.router, prefix="/auth")
# app.include_router(candidates.router, prefix="/candidates")