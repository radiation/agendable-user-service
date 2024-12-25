from app.db import db
from app.errors import NotFoundError, ValidationError
from app.schemas import meeting_schemas
from app.services.meeting_service import (
    add_recurrence_service,
    complete_meeting_service,
    create_meeting_service,
    create_recurring_meetings_service,
    delete_meeting_service,
    get_meeting_service,
    get_meetings_service,
    get_subsequent_meeting_service,
    update_meeting_service,
)
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Middleware to set the attendee for the request
async def get_attendee(request: Request):
    return request.state.attendee


# Create a new meeting
@router.post("/", response_model=meeting_schemas.MeetingRetrieve)
async def create_meeting(
    meeting: meeting_schemas.MeetingCreate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    try:
        return await create_meeting_service(db, meeting)
    except Exception as e:
        raise ValidationError(detail=str(e))


# List all meetings
@router.get("/", response_model=list[meeting_schemas.MeetingRetrieve])
async def get_meetings(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_schemas.MeetingRetrieve]:
    return await get_meetings_service(db, skip, limit)


# Get a meeting by ID
@router.get("/{meeting_id}", response_model=meeting_schemas.MeetingRetrieve)
async def get_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(db.get_db),
    attendee: dict = Depends(get_attendee),
) -> meeting_schemas.MeetingRetrieve:
    meeting = await get_meeting_service(db, meeting_id)
    if not meeting:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

    # Add attendee-specific data (e.g., private notes)
    meeting_data = meeting_schemas.MeetingRetrieve.model_validate(meeting).model_dump()
    meeting_data["private_notes"] = attendee.get("private_notes", "")

    return meeting_schemas.MeetingRetrieve(**meeting_data)


# Update an existing meeting
@router.put("/{meeting_id}", response_model=meeting_schemas.MeetingRetrieve)
async def update_meeting(
    meeting_id: int,
    meeting: meeting_schemas.MeetingUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    updated_meeting = await update_meeting_service(db, meeting_id, meeting)
    if updated_meeting is None:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    return updated_meeting


# Delete a meeting
@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting(meeting_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await delete_meeting_service(db, meeting_id)
    if not success:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")


# Complete a meeting and roll tasks over to the next occurrence
@router.post("/{meeting_id}/complete/", response_model=meeting_schemas.MeetingRetrieve)
async def complete_meeting_route(
    meeting_id: int,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    completed_meeting = await complete_meeting_service(db, meeting_id)
    if not completed_meeting:
        raise NotFoundError(
            detail=f"Meeting with ID {meeting_id} not found or already completed"
        )
    return completed_meeting


# Add a recurrence to a meeting
@router.post(
    "/{meeting_id}/add_recurrence/{recurrence_id}",
    response_model=meeting_schemas.MeetingRetrieve,
)
async def add_recurrence(
    meeting_id: int,
    recurrence_id: int,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    meeting = await add_recurrence_service(db, meeting_id, recurrence_id)
    if meeting is None:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    return meeting


# Get the next meeting after a given meeting
@router.get("/{meeting_id}/next/", response_model=meeting_schemas.MeetingRetrieve)
async def next_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    next_meeting = await get_subsequent_meeting_service(db, meeting_id)
    if not next_meeting:
        raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
    return next_meeting


@router.post(
    "/recurring-meetings", response_model=list[meeting_schemas.MeetingRetrieve]
)
async def create_recurring_meetings(
    recurrence_id: int,
    meeting_data: meeting_schemas.MeetingCreateBatch,
    db: AsyncSession = Depends(db.get_db),
):
    return await create_recurring_meetings_service(
        db, recurrence_id, meeting_data.base_meeting, meeting_data.dates
    )
