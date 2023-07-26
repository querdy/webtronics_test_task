import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.db import Base


class ReactionType(enum.Enum):
    like = "like"
    dislike = "dislike"


class Publication(Base):
    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    header: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    reactions = relationship("Reaction", back_populates="publication", uselist=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates='publications')


class Reaction(Base):
    __tablename__ = "reaction"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="reactions")
    publication_id = mapped_column(ForeignKey("publication.id", ondelete="CASCADE"))
    publication = relationship("Publication", back_populates="reactions")
    type: Mapped[ReactionType] = mapped_column()
