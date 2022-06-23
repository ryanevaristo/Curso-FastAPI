from fastapi import APIRouter

router = APIRouter()

@router.get("/usuario")
async def get_usuario():
    return "Usuario retornado com Sucesso"