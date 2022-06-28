from core.configs import settings
from sqlalchemy import Column, String, Integer

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'cursos'
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email : str = Column(String)
    senha : str = Column(String)
