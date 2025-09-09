from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import create_tables, delete_tables
from app.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База данных готова")
    yield
    await delete_tables()
    print("База данных очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)