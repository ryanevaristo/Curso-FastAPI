
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from core.configs import settings

#Criar conexão com a url do banco de dados
engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
    bind=engine
)