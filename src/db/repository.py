from sqlalchemy import select, delete, update
from src.db.database import TaskOrm, new_session
from src.api.schemas.schemas import STaskAdd, STask


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
    
    @classmethod
    async def update_task(cls, task_id: int, task_data: STaskAdd) -> bool:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            existing_task = result.scalar_one_or_none()

            if not existing_task:
                return False
            
            update_query = (
                update(TaskOrm)
                .where(TaskOrm.id == task_id)
                .values(**task_data.model_dump())
            )

            await session.execute(update_query)
            await session.commit()
            return True

    @classmethod
    async def delete_task(cls, task_id: int) -> STask | None:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(query)
            existing_task = result.scalar_one_or_none()
            
            if not existing_task:
                return False

            delete_query = delete(TaskOrm).where(TaskOrm.id == task_id)
            await session.execute(delete_query)
            await session.commit()
            return True

    @classmethod
    async def delete_all_tasks(cls) -> int:
        async with new_session() as session:
            count_query = select(TaskOrm)
            count_result = await session.execute(count_query)
            task_count = len(count_result.scalars().all())

            delete_query = delete(TaskOrm)
            await session.execute(delete_query)
            await session.commit()
            return task_count