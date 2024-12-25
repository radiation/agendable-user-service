from typing import List

from app.db import db
from app.repositories.meeting_task_repository import MeetingTaskRepository
from app.schemas.meeting_task_schemas import (
    MeetingTaskCreate,
    MeetingTaskRetrieve,
    MeetingTaskUpdate,
)
from app.services.meeting_task_service import (
    create_meeting_task_service,
    delete_meeting_task_service,
    get_meeting_task_service,
    get_tasks_by_meeting_service,
    update_meeting_task_service,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=MeetingTaskRetrieve)
async def create_meeting_task(
    task: MeetingTaskCreate, db: AsyncSession = Depends(db.get_db)
) -> MeetingTaskRetrieve:
    return await create_meeting_task_service(db, task)


@router.get("/", response_model=List[MeetingTaskRetrieve])
async def read_meeting_tasks(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[MeetingTaskRetrieve]:
    repo = MeetingTaskRepository(db)
    tasks = await repo.get_all(skip=skip, limit=limit)
    return [MeetingTaskRetrieve.model_validate(task) for task in tasks]


@router.get("/{meeting_task_id}", response_model=MeetingTaskRetrieve)
async def get_meeting_task(
    meeting_task_id: int, db: AsyncSession = Depends(db.get_db)
) -> MeetingTaskRetrieve:
    return await get_meeting_task_service(db, meeting_task_id)


@router.put("/{meeting_task_id}", response_model=MeetingTaskRetrieve)
async def update_meeting_task(
    meeting_task_id: int,
    meeting_task: MeetingTaskUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> MeetingTaskRetrieve:
    return await update_meeting_task_service(db, meeting_task_id, meeting_task)


@router.delete("/{meeting_task_id}", status_code=204)
async def delete_meeting_task(
    meeting_task_id: int, db: AsyncSession = Depends(db.get_db)
):
    return await delete_meeting_task_service(db, meeting_task_id)


@router.get("/by_meeting/{meeting_id}", response_model=List[MeetingTaskRetrieve])
async def read_tasks_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[MeetingTaskRetrieve]:
    return await get_tasks_by_meeting_service(db, meeting_id)
