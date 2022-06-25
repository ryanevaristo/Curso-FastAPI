from fastapi import APIRouter
from api.v1.endpoints import curso

api_router = APIRouter()
api_router.include_router(curso.route, prefix="/cursos", tags=['Cursos'])