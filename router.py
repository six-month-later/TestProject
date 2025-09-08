from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from repository import TaskRepository
from schemas import STask, STaskAdd, STaskID, Calculator

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
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

@router.post("/add_task")
async def add_task(task: STaskAdd = Depends()) -> STaskID:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}

@router.get("/get_tasks")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks

@router.get("/get_task_by_id/{task_id}")
async def get_tasks_by_id(task_id: int) -> STask | None:
    task = await TaskRepository.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tasl not found")
    return task

@router.patch("/update_task/{task_id}")
async def update_task(task_id: int, task_data: STaskAdd) -> dict:
    success = await TaskRepository.update_task(task_id, task_data)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "message": "Task updated"}

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id: int) -> dict:
    success = await TaskRepository.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "message": "Task deleted"}

@router.delete("/delete_all_tasks")
async def delete_all_tasks() -> dict:
    deleted_count = await TaskRepository.delete_all_tasks()
    return {"success": True, "deleted_count": deleted_count}