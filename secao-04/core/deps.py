from ast import Import
from email.generator import Generator
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        session.close()