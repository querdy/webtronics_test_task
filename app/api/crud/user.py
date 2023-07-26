from typing import Any

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.schema.user import CreateUserSchema
from app.exceptions import UsernameAlreadyExistsError


async def create_user(db: AsyncSession, user: CreateUserSchema) -> Any:
    try:
        created_user = await db.scalar(
            insert(models.User)
            .values(
                login=user.login,
                hashed_password=pbkdf2_sha256.hash(user.password),
                email=user.email,
            )
            .returning(models.User)
        )
        await db.commit()
        return created_user
    except IntegrityError:
        raise UsernameAlreadyExistsError("Пользователь с таким именем уже существует.")


async def get_user_by_login(db: AsyncSession, login: str) -> Any:
    result = await db.scalar(
        select(models.User)
        .where(models.User.login == login)
    )
    return result

