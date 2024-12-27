from app.errors import NotFoundError
from app.repositories.meeting_task_repository import MeetingTaskRepository
from app.schemas.meeting_task_schemas import (
    MeetingTaskCreate,
    MeetingTaskRetrieve,
    MeetingTaskUpdate,
)
from app.schemas.task_schemas import TaskRetrieve


class MeetingTaskService:
    def __init__(self, task_repo: MeetingTaskRepository):
        self.task_repo = task_repo

    async def create_meeting_task(
        self, task_data: MeetingTaskCreate
    ) -> MeetingTaskRetrieve:
        meeting_task = await self.task_repo.create(task_data.model_dump())
        return MeetingTaskRetrieve.model_validate(meeting_task)

    async def get_meeting_task(self, meeting_task_id: int) -> MeetingTaskRetrieve:
        meeting_task = await self.task_repo.get_by_id(meeting_task_id)
        if not meeting_task:
            raise NotFoundError(
                detail=f"MeetingTask with ID {meeting_task_id} not found"
            )
        return MeetingTaskRetrieve.model_validate(meeting_task)

    async def get_meeting_tasks(
        self, skip: int = 0, limit: int = 10
    ) -> list[MeetingTaskRetrieve]:
        meeting_tasks = await self.task_repo.get_all()
        return [MeetingTaskRetrieve.model_validate(task) for task in meeting_tasks]

    async def update_meeting_task(
        self, meeting_task_id: int, update_data: MeetingTaskUpdate
    ) -> MeetingTaskRetrieve:
        meeting_task = await self.task_repo.update(
            meeting_task_id, update_data.model_dump(exclude_unset=True)
        )
        if not meeting_task:
            raise NotFoundError(
                detail=f"MeetingTask with ID {meeting_task_id} not found"
            )
        return MeetingTaskRetrieve.model_validate(meeting_task)

    async def delete_meeting_task(self, meeting_task_id: int) -> bool:
        success = await self.task_repo.delete(meeting_task_id)
        if not success:
            raise NotFoundError(
                detail=f"MeetingTask with ID {meeting_task_id} not found"
            )
        return success

    async def get_tasks_by_meeting(self, meeting_id: int) -> list[TaskRetrieve]:
        tasks = await self.task_repo.get_tasks_by_meeting(meeting_id)
        return [TaskRetrieve.model_validate(task) for task in tasks]
