from fastapi import FastAPI

from app.api.v1.api import api_router
from app.db.base_class import Base
from app.db.session import engine

app = FastAPI(title="FinTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")
