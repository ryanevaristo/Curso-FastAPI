from fastapi import FastAPI
from routes import CursoRouter, UsuarioRouter

app = FastAPI()

app.include_router(CursoRouter.router, tags=['Cursos'])
app.include_router(UsuarioRouter.router, tags=['Usuarios'])