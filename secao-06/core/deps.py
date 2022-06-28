from tokenize import Token
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):
    username_id: Optional[str] = None


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()



async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) ->  UsuarioModel:
    credencial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não foi possivel se autenticar",
        headers={"WWW-Authenticate":"Bearer"},

    )

    #Decodificar o Token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM], options={"verify_aud":False})
        username_id: str = payload.get("sub")

        if username_id is None:
            raise credencial_exception

        token_data: TokenData = TokenData(username_id=username_id)
    except JWTError:
        raise credencial_exception

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username_id))
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credencial_exception

        return usuario