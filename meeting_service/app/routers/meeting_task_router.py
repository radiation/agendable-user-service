from typing import List

from app import db
from app.crud import meeting_task_crud
from app.schemas import meeting_task_schemas as schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting task
@router.post("/", response_model=schemas.MeetingTaskRetrieve)
async def create_meeting_task(
    task: schemas.MeetingTaskCreate, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTaskRetrieve:
    return await meeting_task_crud.create_meeting_task(db=db, task=task)


# List all meeting tasks
@router.get("/", response_model=List[schemas.MeetingTaskRetrieve])
async def read_meeting_tasks(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[schemas.MeetingTaskRetrieve]:
    return await meeting_task_crud.get_meeting_tasks(db=db, skip=skip, limit=limit)


# Get a meeting task by ID
@router.get("/{meeting_task_id}", response_model=schemas.MeetingTaskRetrieve)
async def get_meeting_task(
    meeting_task_id: int, db: AsyncSession = Depends(db.get_db)
) -> schemas.MeetingTaskRetrieve:
    meeting_task = await meeting_task_crud.get_meeting_task(
        db=db, meeting_task_id=meeting_task_id
    )
    if meeting_task is None:
        raise HTTPException(status_code=404, detail="Meeting task not found")
    return meeting_task


# Update an existing meeting task
@router.put("/{meeting_task_id}", response_model=schemas.MeetingTaskRetrieve)
async def update_meeting_task(
    meeting_task_id: int,
    meeting_task: schemas.MeetingTaskUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> schemas.MeetingTaskRetrieve:
    return await meeting_task_crud.update_meeting_task(
        db=db, meeting_task_id=meeting_task_id, meeting_task=meeting_task
    )


# Delete a meeting task
@router.delete("/{meeting_task_id}", status_code=204)
async def delete_meeting_task(
    meeting_task_id: int, db: AsyncSession = Depends(db.get_db)
):
    success = await meeting_task_crud.delete_meeting_task(
        db=db, meeting_task_id=meeting_task_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Meeting task not found")


# Get all tasks for a specific meeting
@router.get(
    "/by_meeting/{meeting_id}", response_model=List[schemas.MeetingTaskRetrieve]
)
async def read_tasks_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[schemas.MeetingTaskRetrieve]:
    return await meeting_task_crud.get_tasks_by_meeting(db=db, meeting_id=meeting_id)
