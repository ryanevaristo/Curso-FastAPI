from fastapi import FastAPI
from api.v1.api import api_router
import uvicorn
from core.configs import settings
app = FastAPI(title="Curso API - FastAPI - SQLalchemy")

app.include_router(api_router)



if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
