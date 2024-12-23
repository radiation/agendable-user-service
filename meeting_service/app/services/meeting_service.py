from datetime import datetime

from app.models import Meeting, MeetingRecurrence
from app.repositories.meeting_repository import MeetingRepository
from app.schemas import meeting_schemas
from dateutil.rrule import rrulestr
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


# Create a new meeting
async def create_meeting_service(
    db: AsyncSession, meeting_data: meeting_schemas.MeetingCreate
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)

    # Validate recurrence_id if provided
    if meeting_data.recurrence_id:
        recurrence = await db.get(MeetingRecurrence, meeting_data.recurrence_id)
        if not recurrence:
            raise HTTPException(
                status_code=400,
                detail=f"Recurrence with ID {meeting_data.recurrence_id} not found",
            )

    # Create the meeting
    meeting = await repo.create_with_recurrence(meeting_data.model_dump())

    # Serialize and return the created meeting
    return meeting_schemas.MeetingRetrieve.model_validate(meeting)


# List all meetings
async def get_meetings_service(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[meeting_schemas.MeetingRetrieve]:
    repo = MeetingRepository(db)
    meetings = await repo.get_all(skip=skip, limit=limit)
    return [
        meeting_schemas.MeetingRetrieve.model_validate(meeting) for meeting in meetings
    ]


# Get a meeting by ID
async def get_meeting_service(
    db: AsyncSession, meeting_id: int
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")
    return meeting_schemas.MeetingRetrieve.model_validate(meeting)


# Update a meeting
async def update_meeting_service(
    db: AsyncSession, meeting_id: int, meeting_data: meeting_schemas.MeetingUpdate
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    for key, value in meeting_data.model_dump(exclude_unset=True).items():
        setattr(meeting, key, value)

    await db.commit()
    await db.refresh(meeting)
    return meeting_schemas.MeetingRetrieve.model_validate(meeting)


# Delete a meeting
async def delete_meeting_service(db: AsyncSession, meeting_id: int) -> bool:
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        return False
    await repo.delete(meeting_id)
    return True


# Complete a meeting
async def complete_meeting_service(
    db: AsyncSession, meeting_id: int
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    meeting.completed = True
    await db.commit()
    await db.refresh(meeting)
    return meeting_schemas.MeetingRetrieve.model_validate(meeting)


# Add a recurrence to a meeting
async def add_recurrence_service(
    db: AsyncSession, meeting_id: int, recurrence_id: int
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    meeting.recurrence_id = recurrence_id
    await db.commit()
    await db.refresh(meeting)
    return meeting_schemas.MeetingRetrieve.model_validate(meeting)


# Get the next meeting in the series
async def get_subsequent_meeting_service(
    db: AsyncSession, meeting_id: int, after_date: datetime = datetime.now()
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)

    # Fetch the meeting and ensure it exists
    meeting = await repo.get_by_id_with_recurrence(meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail=f"Meeting {meeting_id} not found")

    # Validate recurrence ID
    if not meeting.recurrence_id:
        raise HTTPException(
            status_code=400,
            detail=f"Meeting {meeting_id} does not have a recurrence set",
        )

    # Fetch the recurrence object and validate
    recurrence = await db.get(MeetingRecurrence, meeting.recurrence_id)
    if not recurrence:
        raise HTTPException(
            status_code=400,
            detail=f"Recurrence with ID {meeting.recurrence_id} not found",
        )

    # Find the next meeting in the series
    next_meeting = await repo.get_meetings_with_recurrence(
        recurrence_id=meeting.recurrence_id, after_date=after_date
    )

    # If no future meeting exists, create the next one
    if not next_meeting:
        next_meeting = await create_subsequent_meeting_service(db, meeting)
    else:
        next_meeting = next_meeting[0]

    # Return the serialized meeting
    return meeting_schemas.MeetingRetrieve.model_validate(next_meeting)


# Create the next meeting in the series
async def create_subsequent_meeting_service(
    db: AsyncSession, meeting: Meeting
) -> meeting_schemas.MeetingRetrieve:
    repo = MeetingRepository(db)

    # Validate the meeting object
    if not meeting:
        raise HTTPException(status_code=400, detail="Meeting is missing")
    if not meeting.recurrence_id:
        raise HTTPException(
            status_code=400, detail="Meeting does not have a recurrence set"
        )

    # Fetch the recurrence object
    recurrence = await db.get(MeetingRecurrence, meeting.recurrence_id)
    if not recurrence:
        raise HTTPException(
            status_code=404,
            detail=f"Recurrence with ID {meeting.recurrence_id} not found",
        )

    # Calculate the next meeting date using the recurrence rule
    try:
        rule = rrulestr(recurrence.rrule, dtstart=meeting.start_date)
        next_meeting_date = rule.after(meeting.start_date, inc=False)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error parsing recurrence rule: {str(e)}"
        )

    if not next_meeting_date:
        raise HTTPException(
            status_code=400, detail="No future dates found in the recurrence rule"
        )

    # Calculate the end date and duration
    duration = meeting.end_date - meeting.start_date if meeting.end_date else None
    next_meeting_end_date = next_meeting_date + duration if duration else None

    # Prepare the MeetingCreate schema
    meeting_data = meeting_schemas.MeetingCreate(
        title=meeting.title,
        start_date=next_meeting_date,
        end_date=next_meeting_end_date,
        duration=meeting.duration,
        location=meeting.location,
        notes=meeting.notes,
        recurrence_id=meeting.recurrence_id,
    )

    # Create the new meeting using the repository
    new_meeting = await repo.create(meeting_data.model_dump())
    return meeting_schemas.MeetingRetrieve.model_validate(new_meeting)
