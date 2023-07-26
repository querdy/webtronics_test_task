from pydantic import BaseModel

from app.models import ReactionType


class ReactionSchema(BaseModel):
    publication_id: int
    user_id: int
    type: ReactionType

    class Config:
        orm_mode = True


class UserReactionSchema(BaseModel):
    user_id: int
    type: ReactionType

    class Config:
        orm_mode = True


class PublicationReactionSchema(BaseModel):
    publication_id: int
    type: ReactionType

    class Config:
        orm_mode = True

