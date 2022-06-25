
from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    import models.curso_model
    print("criando tabelas no banco de dados .....")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DB_BASE_MODEL.metadata.drop_all)
        await conn.run_sync(settings.DB_BASE_MODEL.metadata.create_all)
    
    print("tabelas criada com sucesso !!")


if __name__ == '__main__':
    import asyncio 
    
    asyncio.get_event_loop().run_until_complete(create_tables())