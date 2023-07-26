from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.crud.reaction import create_reaction, delete_reaction
from app.api.schema.reaction import PublicationReactionSchema, ReactionSchema
from app.database.db import get_session
from app.models import User
from app.services.redis import update_redis_reactions
from app.services.user import get_current_user

router = APIRouter(prefix="/reaction", tags=["Reaction"])


@router.post("/", response_model=ReactionSchema, status_code=status.HTTP_201_CREATED)
async def create_reaction_route(
        reaction: PublicationReactionSchema,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    saved_reaction = await create_reaction(db=db, reaction=reaction, user_id=current_user.id)
    await update_redis_reactions(db=db, publication_id=saved_reaction.publication_id)
    return saved_reaction


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reaction_route(
        publication_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    await delete_reaction(db=db, publication_id=publication_id, user_id=current_user.id)
    await update_redis_reactions(db=db, publication_id=publication_id)

