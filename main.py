from api.api import api_router
from api.limiter import limiter
from api.auth import get_api_key
from database import models
from database.session import engine
from config import settings
from fastapi import (Depends,
                     FastAPI)
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,
                          _rate_limit_exceeded_handler)

app.include_router(api_router, dependencies=[Depends(get_api_key)])

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS
    )

app.include_router(api_router)
