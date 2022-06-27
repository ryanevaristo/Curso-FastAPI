from multiprocessing.pool import ApplyResult
from typing import List
from fastapi import APIRouter, Query, status, Depends, HTTPException, Response
import sqlalchemy

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.CursoModel import CursoModel
from core.deps import get_session

from sqlmodel.sql.expression import Select, SelectOfScalar
# Bypass warning SQLModel select
SelectOfScalar.innerit_cache = True
Select.innerit_cache = True
#fim bypass

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo,
    aulas=curso.aulas,
    horas=curso.horas)

    db.add(novo_curso)
    await db.commit()
    return novo_curso


@router.get("/", response_model=List[CursoModel])
async def get_cursos(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        
        return cursos


@router.get("/{id_curso}", response_model=CursoModel, status_code=status.HTTP_200_OK)
async def get_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(id_curso == CursoModel.id)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail="Curso não Encontrado....", status_code=status.HTTP_404_NOT_FOUND)



@router.put("/{id_curso}", status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel)
async def put_curso(id_curso: int,curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(id_curso == CursoModel.id)
        result = await session.execute(query)
        curso_up: CursoModel = result.scalar_one_or_none()

        if curso_up:
            curso_up.titulo=curso.titulo
            curso_up.aulas=curso.aulas
            curso_up.horas=curso.horas
            await session.commit()
            return curso_up
        else:
            raise HTTPException(detail="Curso não Encontrado....", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{id_curso}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(id_curso == CursoModel.id)
        result = await session.execute(query)
        curso_delete: CursoModel = result.scalar_one_or_none()

        if curso_delete:
            await session.delete(curso_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não Encontrado....", status_code=status.HTTP_404_NOT_FOUND)
