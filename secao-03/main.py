from time import sleep
from typing import Any, List
from fastapi import Depends, FastAPI,status,HTTPException,Path
from fastapi.responses import JSONResponse, Response
import uvicorn
from models import Curso, cursos

app = FastAPI(
    title="Api de Cursos",
    version="0.0.1",
    description="api de estudos sobre FastAPI"
)

#banco


#injeção de dependêcias
def fake_db():
    try:
        print("carregando curso")
        sleep(1)
    finally:
        print("carregando curso:")
        sleep(0.5)

@app.get("/cursos",
    summary="retorna todos os cursos no banco",
    response_model=List[Curso]
)
def get_cursos():
    print(cursos)
    return cursos


@app.get(
    "/cursos/{id_curso}",
    summary="retorna um unico curso",
    response_model=List[Curso]
)
async def get_curso(db: Any = Depends(fake_db) ,id_curso:int | None = Path(default=None, title="Busca por ID do Curso" ,description="tem que ser entre 0 e 6", gt=0, lt=6)):
    try: # tratando erros 
        curso = cursos[id_curso]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse id não existe. porfavor tente outro")


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1 # gera automaticamente o proximo ID
    curso.id = next_id #cria o novo objeto
    cursos.append(curso)
    return curso

@app.put("/cursos/{id_curso}")
async def put_curso(id_curso: int, curso: Curso, db: Any = Depends(fake_db)):
    if id_curso in cursos: # se o curso não estiver dentro do banco cria um novo
        cursos[id_curso] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="esse curso não existe.")


@app.delete("/cursos/{id_curso}")
async def delete_curso(id_curso : int, db: Any = Depends(fake_db)):
    if id_curso not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="esse curso não existe.")
    else:
        cursos.pop(id_curso)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content=cursos)

#essa função é um query parameters, utilizado para fazer pesquisas por categoria etc 
@app.get("/calculadora")
async def calcular(a : int, b : int, db: Any = Depends(fake_db)):
    soma = a + b
    return soma

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)