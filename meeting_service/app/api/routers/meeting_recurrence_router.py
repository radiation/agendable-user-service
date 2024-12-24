from app.db import db
from app.repositories.meeting_recurrence_repository import MeetingRecurrenceRepository
from app.schemas import meeting_recurrence_schemas, meeting_schemas
from app.services.meeting_recurrence_service import (
    create_recurrence_service,
    delete_recurrence_service,
    get_next_meeting_date,
    get_recurrence_service,
    update_recurrence_service,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting recurrence
@router.post("/", response_model=meeting_recurrence_schemas.MeetingRecurrenceRetrieve)
async def create_meeting_recurrence(
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceCreate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    return await create_recurrence_service(db, meeting_recurrence)


# List all meeting recurrences
@router.get(
    "/", response_model=list[meeting_recurrence_schemas.MeetingRecurrenceRetrieve]
)
async def get_meeting_recurrences(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_recurrence_schemas.MeetingRecurrenceRetrieve]:
    repo = MeetingRecurrenceRepository(db)
    recurrences = await repo.get_all(skip=skip, limit=limit)
    return [
        meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(recurrence)
        for recurrence in recurrences
    ]


# Get a meeting recurrence by ID
@router.get(
    "/{recurrence_id}",
    response_model=meeting_recurrence_schemas.MeetingRecurrenceRetrieve,
)
async def get_meeting_recurrence(
    recurrence_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    return await get_recurrence_service(db, recurrence_id)


# Update an existing meeting recurrence
@router.put(
    "/{recurrence_id}",
    response_model=meeting_recurrence_schemas.MeetingRecurrenceRetrieve,
)
async def update_meeting_recurrence(
    recurrence_id: int,
    meeting_recurrence: meeting_recurrence_schemas.MeetingRecurrenceUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    return await update_recurrence_service(db, recurrence_id, meeting_recurrence)


# Delete a meeting recurrence
@router.delete("/{recurrence_id}", status_code=204)
async def delete_meeting_recurrence(
    recurrence_id: int, db: AsyncSession = Depends(db.get_db)
):
    await delete_recurrence_service(db, recurrence_id)
    return {"detail": "Meeting recurrence deleted successfully"}


# Get the next meeting for a recurrence
@router.get(
    "/next-meeting/{recurrence_id}", response_model=meeting_schemas.MeetingRetrieve
)
async def next_meeting(recurrence_id: int, db: AsyncSession = Depends(db.get_db)):
    next_meeting_date = await get_next_meeting_date(db, recurrence_id)
    if not next_meeting_date:
        raise HTTPException(
            status_code=404, detail="No next meeting found or invalid recurrence"
        )
    return next_meeting_date
