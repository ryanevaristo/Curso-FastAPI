from fastapi import FastAPI
import uvicorn
from core.configs import settings
from api.v1.api import api_router

app: FastAPI = FastAPI(title='Curso API =FastAPI SQL Model')
app.include_router(api_router)


if __name__ == '__main__':
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                 reload=True)
