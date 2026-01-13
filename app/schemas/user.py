from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel): 

    # E-mail é comum a todas operacoes do usuário
    email: EmailStr

class UserCreate(UserBase):

    # herda e-mail e adiciona o campo de senha
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True