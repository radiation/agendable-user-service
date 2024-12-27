from datetime import datetime

from app.errors import NotFoundError
from app.models import MeetingTask
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schemas import TaskCreate, TaskRetrieve, TaskUpdate


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def create_task(self, task_data: TaskCreate) -> TaskRetrieve:
        task = await self.task_repo.create(task_data.model_dump())
        return TaskRetrieve.model_validate(task)

    async def get_task(self, task_id: int) -> TaskRetrieve:
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundError(detail=f"Task with ID {task_id} not found")
        return TaskRetrieve.model_validate(task)

    async def list_tasks(self, skip: int = 0, limit: int = 10) -> list[TaskRetrieve]:
        tasks = await self.task_repo.get_all(skip=skip, limit=limit)
        return [TaskRetrieve.model_validate(task) for task in tasks]

    async def update_task(self, task_id: int, update_data: TaskUpdate) -> TaskRetrieve:
        task = await self.task_repo.update(
            task_id, update_data.model_dump(exclude_unset=True)
        )
        if not task:
            raise NotFoundError(detail=f"Task with ID {task_id} not found")
        return TaskRetrieve.model_validate(task)

    async def delete_task(self, task_id: int) -> bool:
        success = await self.task_repo.delete(task_id)
        if not success:
            raise NotFoundError(detail=f"Task with ID {task_id} not found")
        return success

    async def get_tasks_by_user(self, user_id: int) -> list[TaskRetrieve]:
        tasks = await self.task_repo.get_tasks_by_user(user_id)
        return [TaskRetrieve.model_validate(task) for task in tasks]

    async def mark_task_complete(self, task_id: int) -> TaskRetrieve:
        task = await self.task_repo.mark_task_complete(task_id)
        if not task:
            raise NotFoundError(detail=f"Task with ID {task_id} not found")
        return TaskRetrieve.model_validate(task)

    async def create_new_meeting_task(
        self,
        meeting_id: int,
        task_title: str,
        assignee_id: int,
        due_date: datetime = None,
    ) -> MeetingTask:
        # TODO: Logic to create a meeting task
        pass
