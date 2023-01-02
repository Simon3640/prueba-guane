from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, SecretStr, validator

regex = "^[A-Za-zÁÉÍÓÚáéíóúñÑ ]*$"


class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        regex=regex
    )
    names: str = Field(
        min_length=3,
        max_length=50,
        regex=regex
    )
    last_names: str = Field(
        min_length=3,
        max_length=50,
        regex=regex
    )
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)

    # We force upper case for search engine optimization
    @validator('username', 'names', 'last_names', 'email')
    def convert_upper(cls, value):
        return value.upper()


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: SecretStr

class UserResponse(UserInDBBase):
    pass