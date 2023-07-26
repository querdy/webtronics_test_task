import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.crud.reaction import get_reactions_by_publication_id
from app.database import redis
from app.models import ReactionType
from app.services.utils import publication_reactions_to_dict
from app.settings import settings


async def update_redis_reactions(db: AsyncSession, publication_id: int) -> dict:
    reactions_db = await get_reactions_by_publication_id(db=db, publication_id=publication_id)
    reactions = publication_reactions_to_dict(reactions_db)
    if settings.USE_REDIS_CACHE:
        await redis.set(publication_id, json.dumps(reactions))
    return reactions


async def get_redis_reactions(publication_id: int) -> dict | None:
    if settings.USE_REDIS_CACHE:
        reactions = await redis.get(publication_id)
        return reactions if reactions is None else json.loads(reactions)


async def get_reactions(db: AsyncSession, publication_id: int) -> dict:
    reactions = await get_redis_reactions(publication_id)
    if reactions is None or len(ReactionType) != len(reactions):
        reactions = await update_redis_reactions(db=db, publication_id=publication_id)
    return reactions
