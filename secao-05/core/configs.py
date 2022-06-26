from pydantic import BaseSettings

class Settings(BaseSettings):
    
    '''
    Configurações do Projeto
    '''

    API_V1_STR : str = 'api/v1'
    DB_URL : str = 'postgresql+asyncpg://postgres:admin@localhost:5432/faculdade'

    class Config:
        case_sensitive = True

settings : Settings = Settings()