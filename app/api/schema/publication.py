from pydantic import BaseModel, Field

from app.models import ReactionType


class CreatePublicationSchema(BaseModel):
    header: str = Field(max_length=128)
    text: str


class UpdatePublicationSchema(CreatePublicationSchema):
    id: int

    class Config:
        orm_mode = True


class ResponsePublicationSchema(UpdatePublicationSchema):
    reactions: dict[ReactionType, int]
    user_id: int

    class Config:
        orm_mode = True




