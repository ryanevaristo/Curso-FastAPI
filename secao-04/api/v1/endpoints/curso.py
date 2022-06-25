from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
import sqlalchemy

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import SchemaCurso
from core.deps import get_session

route = APIRouter()

#POST CURSO
@route.post("/", status_code=status.HTTP_201_CREATED, response_model=SchemaCurso)
async def post_curso(curso: SchemaCurso, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()

    return novo_curso


#GET CURSOS
@route.get("/", response_model=List[SchemaCurso],  status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
    return cursos

#get Curso
@route.get("/{id_curso}", response_model=SchemaCurso, status_code=status.HTTP_200_OK)
async def get_curso(id_curso: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso: List[CursoModel] = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


#PUT CURSO
@route.put("/{id_curso}", response_model=SchemaCurso)
async def put_curso(id_curso: int, curso: SchemaCurso, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso_up: List[CursoModel] = result.scalar_one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()
            return curso_up
        else:
            raise HTTPException(detail="Curso não Encontrado", status_code=status.HTTP_404_NOT_FOUND)


# DELETE CURSO
@route.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso_delete: List[CursoModel] = result.scalar_one_or_none()

        if curso_delete:
            await session.delete(curso_delete)
            
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não Encontrado", status_code=status.HTTP_404_NOT_FOUND)