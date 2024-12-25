from datetime import datetime

from app.errors import NotFoundError
from app.models import MeetingTask
from app.repositories.task_repository import TaskRepository
from app.schemas.task_schemas import TaskCreate, TaskRetrieve, TaskUpdate
from app.services.meeting_service import (
    get_meeting_service,
    get_subsequent_meeting_service,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task_service(db: AsyncSession, task_data: TaskCreate) -> TaskRetrieve:
    repo = TaskRepository(db)
    task = await repo.create(task_data.model_dump())
    return TaskRetrieve.model_validate(task)


async def get_task_service(db: AsyncSession, task_id: int) -> TaskRetrieve:
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise NotFoundError(detail=f"Task with ID {task_id} not found")
    return TaskRetrieve.model_validate(task)


async def update_task_service(
    db: AsyncSession, task_id: int, update_data: TaskUpdate
) -> TaskRetrieve:
    repo = TaskRepository(db)
    task = await repo.update(task_id, update_data.model_dump(exclude_unset=True))
    if not task:
        raise NotFoundError(detail=f"Task with ID {task_id} not found")
    return TaskRetrieve.model_validate(task)


async def delete_task_service(db: AsyncSession, task_id: int) -> bool:
    repo = TaskRepository(db)
    success = await repo.delete(task_id)
    if not success:
        raise NotFoundError(detail=f"Task with ID {task_id} not found")
    return success


async def get_tasks_by_user_service(
    db: AsyncSession, user_id: int
) -> list[TaskRetrieve]:
    repo = TaskRepository(db)
    tasks = await repo.get_tasks_by_user(user_id)
    return [TaskRetrieve.model_validate(task) for task in tasks]


async def mark_task_complete_service(db: AsyncSession, task_id: int) -> TaskRetrieve:
    repo = TaskRepository(db)
    task = await repo.mark_task_complete(task_id)
    if not task:
        raise NotFoundError(detail=f"Task with ID {task_id} not found")
    return TaskRetrieve.model_validate(task)


# Create a new task and assign it to a meeting via a meeting task
async def create_new_meeting_task(
    db: AsyncSession,
    meeting_id: int,
    task_title: str,
    assignee_id: int,
    due_date: datetime = None,
) -> MeetingTask:
    # Fetch the meeting
    meeting = await get_meeting_service(db, meeting_id)
    if not meeting:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

    # Determine the due date for the task
    if not due_date:
        next_meeting = await get_subsequent_meeting_service(
            db, meeting_id=meeting.id, after_date=meeting.end_date
        )
        due_date = next_meeting.start_date if next_meeting else None

    # Create the task using the service layer
    new_task_data = TaskCreate(
        title=task_title,
        assignee_id=assignee_id,
        due_date=due_date,
        completed=False,
    )
    new_task = await create_task_service(db, new_task_data)

    # Link the task with the meeting
    new_meeting_task = MeetingTask(meeting_id=meeting_id, task_id=new_task.id)
    db.add(new_meeting_task)
    await db.commit()
    await db.refresh(new_meeting_task)

    return new_meeting_task
