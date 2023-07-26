from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.schema.publication import ResponsePublicationSchema
from app.services.redis import get_reactions


async def build_response_publication_schema(db: AsyncSession, publication: models.Publication):
    reactions = await get_reactions(db=db, publication_id=publication.id)
    return ResponsePublicationSchema(
        id=publication.id,
        header=publication.header,
        text=publication.text,
        user_id=publication.user_id,
        reactions=reactions
    )
