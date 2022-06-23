from fastapi import APIRouter

router = APIRouter()

@router.get("/cursos")
async def get_cursos():
    return "Seus Cursos foi retornado com Sucesso!"