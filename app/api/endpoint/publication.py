from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.crud.publication import create_publication, get_all_publication, get_publication, delete_publication, \
    update_publication
from app.api.endpoint import reaction
from app.api.schema.publication import CreatePublicationSchema, ResponsePublicationSchema, UpdatePublicationSchema
from app.database.db import get_session
from app.models import User
from app.services.build_schema import build_response_publication_schema
from app.services.user import get_current_user

router = APIRouter(prefix="/publication")
router.include_router(reaction.router)


@router.get("/", response_model=list[ResponsePublicationSchema], status_code=status.HTTP_200_OK, tags=['Publication'])
async def get_publications_route(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session)
):
    publications = await get_all_publication(db=db)
    return [await build_response_publication_schema(db=db, publication=publication) for publication in publications]


@router.get("/{publication_id}", response_model=ResponsePublicationSchema, status_code=status.HTTP_200_OK, tags=['Publication'])
async def get_publication_route(
        publication_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):

    publication = await get_publication(db=db, publication_id=publication_id)
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Публикация с указанным id не существует"
        )
    return await build_response_publication_schema(db=db, publication=publication)


@router.post("/", response_model=ResponsePublicationSchema, status_code=status.HTTP_201_CREATED, tags=['Publication'])
async def create_publication_route(
        publication: CreatePublicationSchema,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    created_publication = await create_publication(db=db, publication=publication, user_id=current_user.id)
    return await build_response_publication_schema(db=db, publication=created_publication)


@router.patch("/", response_model=ResponsePublicationSchema, status_code=status.HTTP_200_OK, tags=['Publication'])
async def update_publication_route(
        publication: UpdatePublicationSchema,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    updated_publication = await update_publication(db=db, publication=publication, user_id=current_user.id)
    return await build_response_publication_schema(db=db, publication=updated_publication)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, tags=['Publication'])
async def delete_publication_route(
        publication_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    await delete_publication(db=db, publication_id=publication_id, user_id=current_user.id)

