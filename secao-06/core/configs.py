from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/faculdade"
    DBBaseModel= declarative_base()

    JWT_SECRET: str = '1brc1ffXkqtAN6L1Y3IEAqt06flzwigbYg'
    
    '''
        Gerar token automatico:
        import secrets
        token: str = secrets.token_urlsafe(25)

    '''
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings() 