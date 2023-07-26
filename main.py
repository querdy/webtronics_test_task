from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.handlers import exception_handler, request_validation_error_handler
from app.api.router import api_router
from app.exceptions import BaseWebtronicsError

from app.settings import settings

app = FastAPI(
    title="Webtronic test task",
    docs_url=f"{settings.API_STR}/docs",
    exception_handlers={
        RequestValidationError: request_validation_error_handler,
        BaseWebtronicsError: exception_handler,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)
