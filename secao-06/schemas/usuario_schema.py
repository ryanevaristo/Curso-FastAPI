from pydantic import BaseModel, EmailStr
from typing import Optional, List

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):

    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    is_admin: bool = False 

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaArtigo(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    is_admin: Optional[bool] 