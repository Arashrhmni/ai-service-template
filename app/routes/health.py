from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.redis_client import redis_client

router = APIRouter()


@router.get("/health")
async def health(response: Response, session: AsyncSession = Depends(get_session)):
    result = {"db": "unknown", "redis": "unknown"}
    healthy = True

    try:
        await session.execute(text("SELECT 1"))
        result["db"] = "ok"
    except Exception as exc:
        result["db"] = f"error: {exc.__class__.__name__}"
        healthy = False

    try:
        await redis_client.ping()
        result["redis"] = "ok"
    except Exception as exc:
        result["redis"] = f"error: {exc.__class__.__name__}"
        healthy = False

    response.status_code = status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return result
