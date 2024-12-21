from typing import List

from app import db
from app.crud import meeting_attendee_crud
from app.schemas import meeting_attendee_schemas, meeting_schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new meeting attendee
@router.post("/", response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve)
async def create_meeting_attendee(
    attendee: meeting_attendee_schemas.MeetingAttendeeCreate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    return await meeting_attendee_crud.create_meeting_attendee(db=db, attendee=attendee)


# List all meeting attendees
@router.get("/", response_model=List[meeting_attendee_schemas.MeetingAttendeeRetrieve])
async def get_meeting_attendees(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_attendee_schemas.MeetingAttendeeRetrieve]:
    return await meeting_attendee_crud.get_meeting_attendees(
        db=db, skip=skip, limit=limit
    )


# Get a meeting attendee by ID
@router.get(
    "/{meeting_attendee_id}",
    response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve,
)
async def get_meeting_attendee(
    meeting_attendee_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    attendee = await meeting_attendee_crud.get_meeting_attendee(
        db=db, meeting_attendee_id=meeting_attendee_id
    )
    if not attendee:
        raise HTTPException(status_code=404, detail="Meeting attendee not found")
    return attendee


# Update an existing meeting attendee
@router.put(
    "/{meeting_attendee_id}",
    response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve,
)
async def update_meeting_attendee(
    meeting_attendee_id: int,
    meeting_attendee: meeting_attendee_schemas.MeetingAttendeeUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    updated_attendee = await meeting_attendee_crud.update_meeting_attendee(
        db=db,
        meeting_attendee_id=meeting_attendee_id,
        meeting_attendee=meeting_attendee,
    )
    if not updated_attendee:
        raise HTTPException(status_code=404, detail="Meeting attendee not found")
    return updated_attendee


# Delete a meeting attendee
@router.delete("/{meeting_attendee_id}", status_code=204)
async def delete_meeting_attendee(
    meeting_attendee_id: int, db: AsyncSession = Depends(db.get_db)
):
    success = await meeting_attendee_crud.delete_meeting_attendee(
        db=db, meeting_attendee_id=meeting_attendee_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Meeting attendee not found")


# Get all attendees for a specific meeting
@router.get(
    "/by_meeting/{meeting_id}",
    response_model=List[meeting_attendee_schemas.MeetingAttendeeRetrieve],
)
async def read_attendees_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_attendee_schemas.MeetingAttendeeRetrieve]:
    return await meeting_attendee_crud.get_attendees_by_meeting(
        db=db, meeting_id=meeting_id
    )


# Get all meetings for a specific user
@router.get(
    "/user_meetings/{user_id}", response_model=List[meeting_schemas.MeetingRetrieve]
)
async def read_meetings_by_user(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_schemas.MeetingRetrieve]:
    return await meeting_attendee_crud.get_meetings_by_user(db=db, user_id=user_id)
