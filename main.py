from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.endpoints.routers import router as tasks_router
from src.core.config import load_config
from src.db.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База данных готова")
    yield
    await delete_tables()
    print("База данных очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

config = load_config()

if config.debug:
    app.debug = True
else:
    app.debug = False
