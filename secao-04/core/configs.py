from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    '''
        configurações do projeto

    '''
    API_V1_STR : str = 'api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:admin@localhost:5432/faculdade"
    DB_BASE_MODEL = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()