from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
import redis.asyncio as redis
from app.core.config import settings

router = APIRouter()

@router.get("")
async def health_check():
    db_ok = False
    redis_ok = False
    
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        pass
        
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
        redis_ok = True
    except Exception:
        pass

    if db_ok and redis_ok:
        return {"status": "ok", "db": "up", "redis": "up"}
    else:
        return {"status": "error", "db": "up" if db_ok else "down", "redis": "up" if redis_ok else "down"}
