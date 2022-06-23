from multiprocessing.sharedctypes import Value
from posixpath import split
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id : int | None = None
    titulo : str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(value: str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError("O titulo deve ter mais do que 2 palavras")
    
        return value

    @validator('aulas')
    def validar_aula(value: int): 
        if value > 200:
            raise ValueError("Esse curso ultrapassou o limite de horas")

        return value

    @validator('horas')
    def validar_horas(value: int): 
        if value > 1000:
            raise ValueError("Esse curso ultrapassou o limite de horas")

        return value

cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=20, horas=260),
    Curso(id=2, titulo="Programação em Python", aulas=76, horas=320),
    Curso(id=3, titulo="Programação em Java", aulas=100, horas=600)

]
