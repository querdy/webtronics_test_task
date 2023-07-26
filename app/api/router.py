from fastapi import APIRouter

from app.api.endpoint import publication, user

api_router = APIRouter()
api_router.include_router(publication.router)
api_router.include_router(user.router)
