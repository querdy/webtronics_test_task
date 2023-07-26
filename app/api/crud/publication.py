from typing import Any

from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.schema.publication import CreatePublicationSchema, UpdatePublicationSchema
from app.exceptions import BadUserError, BadIdError


async def create_publication(db: AsyncSession, publication: CreatePublicationSchema, user_id: int) -> Any:
    saved_publication = await db.scalar(
        insert(models.Publication)
        .values(**publication.dict(), user_id=user_id)
        .returning(models.Publication)
    )
    await db.commit()
    return saved_publication


async def get_publication(db: AsyncSession, publication_id: int) -> Any:
    result = await db.scalar(
        select(models.Publication)
        .where(models.Publication.id == publication_id)
    )
    return result


async def get_all_publication(db: AsyncSession) -> Any:
    result = await db.scalars(
        select(models.Publication)
    )
    return result


async def delete_publication(db: AsyncSession, publication_id: int, user_id: int) -> None:
    publication_in_db = await get_publication(db=db, publication_id=publication_id)
    if publication_in_db is None:
        raise BadIdError("Публикация с указанным id не существует")
    if publication_in_db.user_id != user_id:
        raise BadUserError("Нельзя удалить созданную другим пользователем публикацию")

    await db.execute(
        delete(models.Publication)
        .where(models.Publication.id == publication_id)
    )
    await db.commit()


async def update_publication(db: AsyncSession, publication: UpdatePublicationSchema, user_id: int) -> Any:
    publication_in_db = await get_publication(db=db, publication_id=publication.id)
    if publication_in_db is None:
        raise BadIdError("Публикация с указанным id не существует")
    if publication_in_db.user_id != user_id:
        raise BadUserError("Нельзя изменить созданную другим пользователем публикацию")

    values = {key: value for key, value in publication.dict().items() if value}
    updated_publication = await db.scalar(
        update(models.Publication)
        .where(models.Publication.id == publication.id)
        .values(**values)
        .returning(models.Publication)
    )
    await db.commit()
    return updated_publication
