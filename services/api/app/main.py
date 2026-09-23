from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.projects import router as projects_router
from app.core.config import get_settings
from app.core.product import API_DESCRIPTION
from app.database import get_db

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=API_DESCRIPTION,
)

v1 = APIRouter(prefix="/api/v1")
v1.include_router(projects_router)
app.include_router(v1)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aantoonbaar-api"}


@app.get("/ready", tags=["operations"])
def ready(session: Annotated[Session, Depends(get_db)]) -> dict[str, str]:
    session.execute(text("SELECT 1"))
    return {"status": "ready"}
