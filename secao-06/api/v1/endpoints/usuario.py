import http
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate, UsuarioSchemaArtigo
from core.deps import get_current_user, get_session
from core.auth import autenticar, criar_acesso_token
from core.security import gerar_hash



router = APIRouter()


#usuario logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# POST / Create User
@router.post('/signup', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
                                nome=usuario.nome,
                                sobrenome=usuario.sobrenome,
                                email=usuario.email,
                                senha=gerar_hash(usuario.senha),
                                is_admin = usuario.is_admin
    )
    async with db as session:
        session.add(novo_usuario)
        await session.commit()

        return novo_usuario


#GET USUARIOS
@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session)) -> UsuarioSchemaBase:
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
    
        return usuarios
    


#GET USUARIO
@router.get('/{id_usuario}', response_model=UsuarioSchemaArtigo, status_code=status.HTTP_200_OK)
async def get_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id_usuario)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigo = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail="Usuário não encontrado....", status_code=status.HTTP_404_NOT_FOUND)



#PUT USUARIO
@router.put('/{id_usuario}', response_model=UsuarioSchemaUpdate, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(id_usuario: int,usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id_usuario)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.is_admin:
                usuario_up.is_admin = usuario.is_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash(usuario.senha)

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail="Usuário não encontrado....", status_code=status.HTTP_404_NOT_FOUND)


#DELETE USUARIO
@router.delete('/{id_usuario}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id_usuario)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigo = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário não encontrado....", status_code=status.HTTP_404_NOT_FOUND)


# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": criar_acesso_token(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
