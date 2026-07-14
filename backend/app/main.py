from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import BaseAPIError, api_error_handler
from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.cache.redis_client import redis_client
from app.jobs.scheduler import start_scheduler, scheduler
from app.middleware.rate_limit import limiter

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.connect()
    start_scheduler()
    yield
    scheduler.shutdown()
    await redis_client.close()

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(BaseAPIError, api_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
