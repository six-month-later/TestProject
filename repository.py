from sqlalchemy import select, delete, update
from db.database import TaskOrm, new_session
from schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            data = task.model_dump()
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id
    
    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks
        
    @classmethod
    async def get_task_by_id(cls, task_id: int) -> STask | None:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            if task_model:
                return STask.model_validate(task_model)
            return None
    


    # @classmethod
    # async def delete_tasks(cls) -> STask | None:
    #     async with new_session() as session:
    #         query = delete(TaskOrm)
    #         result = await session.
