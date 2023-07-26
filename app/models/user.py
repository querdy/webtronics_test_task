from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database.db import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    publications = relationship("Publication", back_populates="user", uselist=True)
    reactions = relationship("Reaction", back_populates="user", uselist=True)

