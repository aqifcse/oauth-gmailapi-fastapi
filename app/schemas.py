# schemas.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    password: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str