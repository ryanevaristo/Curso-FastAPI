from pydantic import BaseModel as SCBaseModel

class Curso(SCBaseModel):
    id: int | None
    titulo: str
    aulas: int
    horas: int

    class Config:
        orm_mode = True