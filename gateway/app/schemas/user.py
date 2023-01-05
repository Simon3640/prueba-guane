from pydantic import BaseModel, EmailStr, Field

regex = "^[A-Za-zÁÉÍÓÚáéíóúñÑ ]*$"


class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        regex="^[A-Za-z0-9ÁÉÍÓÚáéíóúñÑ ]*$"
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


class UserUpdate(UserBase):
    pass