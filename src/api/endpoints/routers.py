from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.api.schemas.schemas import Calculator, STask, STaskAdd, STaskID
from src.core.logger import logger
from src.db.repository import TaskRepository

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


@router.get("/info")
async def start_data():
    return {"message": "Это мой первый проект FastAPI!"}


@router.get("/")
async def into_file():
    return FileResponse("public/index.html")


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


@router.post("/calculate")
async def sum_two_numbers(nums: Calculator = Depends()):
    first_number = int(nums.num1)
    logger.info("Добавили первое число")
    second_number = int(nums.num2)
    logger.info("Добавили второе число")
    result_sum = first_number + second_number
    logger.info("Сумма посчитана успешно")
    return {"result": result_sum}
