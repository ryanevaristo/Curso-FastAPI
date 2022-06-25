from core.configs import settings
from sqlalchemy import Column, Integer, String

class CursoModel(settings.DB_BASE_MODEL):
    __tablename__ = 'cursos'

    id  = Column(Integer, primary_key=True)
    titulo  =  Column(String)
    aulas= Column(Integer)
    horas = Column(Integer)
    