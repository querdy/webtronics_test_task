from pydantic import validator, BaseModel, EmailStr

from app.api.schema.mixins import FormParserMixin
from app.services.hunter_io import verifying_email


class AuthUserSchema(BaseModel):
    login: str
    password: str


class ResponseUserSchema(BaseModel):
    login: str
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(FormParserMixin, BaseModel):
    login: str
    password: str
    confirm_password: str
    email: EmailStr

    @validator('login')
    def name_must_not_space(cls, login):
        if ' ' in login:
            raise ValueError('В имени не должно быть пробелов.')
        return login

    @validator('confirm_password')
    def passwords_match(cls, c_psw, values):
        if 'password' in values and c_psw != values['password']:
            raise ValueError('Пароли не совпадают.')
        return c_psw


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
