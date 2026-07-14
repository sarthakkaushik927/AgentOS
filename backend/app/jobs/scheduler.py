from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

import redis

_redis_client = redis.from_url(settings.REDIS_URL)
_store = RedisJobStore()
_store.redis = _redis_client

jobstores = {
    'default': _store
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

async def dummy_cleanup_job():
    logger.info("Running token/session cleanup job...")

def start_scheduler():
    scheduler.add_job(dummy_cleanup_job, 'interval', minutes=60, id='cleanup_job', replace_existing=True)
    scheduler.start()
