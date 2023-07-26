from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.crud.user import create_user, get_user_by_login
from app.api.schema.user import TokenSchema, CreateUserSchema, ResponseUserSchema
from app.database.db import get_session
from app.exceptions import VerifyEmailError
from app.models import User
from app.services.hunter_io import verifying_email
from app.services.user import create_access_token, get_current_user

router = APIRouter(prefix="/user", tags=['User'])


@router.post('/signup', response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def register_new_user_route(
        user: CreateUserSchema = Form(),
        db: AsyncSession = Depends(get_session)
):
    if not await verifying_email(email=user.email):
        raise VerifyEmailError("Указан не существующий Email")
    created_user = await create_user(db, user)
    access_token = create_access_token(data={"sub": created_user.login})
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await get_user_by_login(login=form_data.username, db=db)
    if not user or not pbkdf2_sha256.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверно введен логин или пароль")
    access_token = create_access_token(data={"sub": user.login})
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=ResponseUserSchema, status_code=status.HTTP_200_OK)
async def get_me_route(current_user: User = Depends(get_current_user)):
    return current_user

