from sqlmodel import SQLModel
from core.database import engine


async def create_tables() -> None:
    import models.all_models
    print("Criando tabelas ......")

    async with engine.begin() as connect:
        await connect.run_sync(SQLModel.metadata.drop_all)
        await connect.run_sync(SQLModel.metadata.create_all)
    print('Tabelas Criadas com Sucessos !!')


if __name__ == '__main__':
    import asyncio 
    
    asyncio.get_event_loop().run_until_complete(create_tables())