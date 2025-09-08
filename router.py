from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskID, Calculator

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

# @app.get("/info")
# async def start_data():
#     return {"message": "Это мой первый проект FastAPI!"}


# @app.get("/")
# async def into_file():
#     return FileResponse("public/index.html")


# @app.post("/calculate")
# async def calc_two_numbers(sum: Calculator):
#     # rez = sum[0] + sum[1]
#     return {"message": "Сумма равна"}

@router.post("")
async def add_task(task: STaskAdd = Depends()) -> STaskID:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}

@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks

@router.patch("")
async def get_tasks_by_id() -> STask:
    task = await TaskRepository.get_task_by_id()
    return task