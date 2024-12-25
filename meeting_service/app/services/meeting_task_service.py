from app.repositories.meeting_task_repository import MeetingTaskRepository
from app.schemas.meeting_task_schemas import (
    MeetingTaskCreate,
    MeetingTaskRetrieve,
    MeetingTaskUpdate,
)
from app.schemas.task_schemas import TaskRetrieve
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def create_meeting_task_service(
    db: AsyncSession, task_data: MeetingTaskCreate
) -> MeetingTaskRetrieve:
    repo = MeetingTaskRepository(db)
    meeting_task = await repo.create(task_data.model_dump())
    return MeetingTaskRetrieve.model_validate(meeting_task)


async def get_meeting_task_service(
    db: AsyncSession, meeting_task_id: int
) -> MeetingTaskRetrieve:
    repo = MeetingTaskRepository(db)
    meeting_task = await repo.get_by_id(meeting_task_id)
    if not meeting_task:
        raise HTTPException(status_code=404, detail="Meeting task not found")
    return MeetingTaskRetrieve.model_validate(meeting_task)


async def get_meeting_tasks_service(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingTaskRetrieve]:
    repo = MeetingTaskRepository(db)
    meeting_tasks = await repo.get_all()
    return [MeetingTaskRetrieve.model_validate(task) for task in meeting_tasks]


async def update_meeting_task_service(
    db: AsyncSession, meeting_task_id: int, update_data: MeetingTaskUpdate
) -> MeetingTaskRetrieve:
    repo = MeetingTaskRepository(db)
    meeting_task = await repo.update(
        meeting_task_id, update_data.model_dump(exclude_unset=True)
    )
    if not meeting_task:
        raise HTTPException(status_code=404, detail="Meeting task not found")
    return MeetingTaskRetrieve.model_validate(meeting_task)


async def delete_meeting_task_service(db: AsyncSession, meeting_task_id: int) -> bool:
    repo = MeetingTaskRepository(db)
    success = await repo.delete(meeting_task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meeting task not found")
    return success


async def get_tasks_by_meeting_service(
    db: AsyncSession, meeting_id: int
) -> list[TaskRetrieve]:
    repo = MeetingTaskRepository(db)
    tasks = await repo.get_tasks_by_meeting(meeting_id)
    return [TaskRetrieve.model_validate(task) for task in tasks]
