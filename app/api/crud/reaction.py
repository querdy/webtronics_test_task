from typing import Any

from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.crud.publication import get_publication
from app.api.schema.reaction import PublicationReactionSchema
from app.exceptions import BadUserError, DoubleReactionError, BadIdError, BadUserOrIdError


async def get_reaction_by_user_and_publication(db: AsyncSession, user_id: int, publication_id: int):
    result = await db.scalar(
        select(models.Reaction)
        .where(
            models.Reaction.user_id == user_id,
            models.Reaction.publication_id == publication_id
        )
    )
    return result


async def get_reactions_by_publication_id(db: AsyncSession, publication_id: int):
    result = await db.scalars(
        select(models.Reaction)
        .where(
            models.Reaction.publication_id == publication_id
        )
    )
    return result


async def create_reaction(db: AsyncSession, reaction: PublicationReactionSchema, user_id: int) -> Any:
    publication = await get_publication(db=db, publication_id=reaction.publication_id)
    if publication is None:
        raise BadIdError(f"Публикация с указанным id не существует")
    if publication.user_id == user_id:
        raise BadUserError(f"Нельзя поставить реакцию на собственную публикацию")
    if await get_reaction_by_user_and_publication(db=db, user_id=user_id, publication_id=reaction.publication_id):
        raise DoubleReactionError(f"Нельзя установить две реакции на одну публикацию")

    saved_reaction = await db.scalar(
        insert(models.Reaction)
        .values(**reaction.dict(), user_id=user_id)
        .returning(models.Reaction)
    )
    await db.commit()
    return saved_reaction


async def delete_reaction(db: AsyncSession, publication_id: int, user_id: int) -> None:
    reaction_in_db = await get_reaction_by_user_and_publication(db=db, user_id=user_id, publication_id=publication_id)
    if reaction_in_db is None:
        raise BadUserOrIdError("Публикация не существует, либо у данной публикации нет реакции юзера")
    if reaction_in_db.user_id != user_id:
        raise BadUserError("Нельзя удалить созданную другим пользователем реакцию")

    await db.execute(
        delete(models.Reaction)
        .where(models.Reaction.id == reaction_in_db.id)
    )
    await db.commit()
