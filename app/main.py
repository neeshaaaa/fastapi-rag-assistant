from fastapi import FastAPI

from app.db.database import Base
from app.db.database import engine

from app.api.ingestion import router as ingestion_router
from app.api.chat import router as chat_router
import app.db.models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    ingestion_router,
    prefix="/ingest"
)

app.include_router(
    chat_router,
    prefix="/chat"
)