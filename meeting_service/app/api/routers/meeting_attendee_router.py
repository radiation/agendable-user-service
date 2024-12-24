from typing import List

from app.db import db
from app.schemas import meeting_attendee_schemas, meeting_schemas
from app.services.meeting_attendee_service import (
    create_meeting_attendee_service,
    delete_meeting_attendee_service,
    get_attendees_by_meeting_service,
    get_meeting_attendee_service,
    get_meeting_attendees_service,
    get_meetings_by_user_service,
    update_meeting_attendee_service,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve)
async def create_meeting_attendee(
    attendee: meeting_attendee_schemas.MeetingAttendeeCreate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    return await create_meeting_attendee_service(db, attendee)


@router.get("/", response_model=List[meeting_attendee_schemas.MeetingAttendeeRetrieve])
async def get_meeting_attendees(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_attendee_schemas.MeetingAttendeeRetrieve]:
    return await get_meeting_attendees_service(db, skip, limit)


@router.get(
    "/{meeting_attendee_id}",
    response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve,
)
async def get_meeting_attendee(
    meeting_attendee_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    return await get_meeting_attendee_service(db, meeting_attendee_id)


@router.put(
    "/{meeting_attendee_id}",
    response_model=meeting_attendee_schemas.MeetingAttendeeRetrieve,
)
async def update_meeting_attendee(
    meeting_attendee_id: int,
    attendee: meeting_attendee_schemas.MeetingAttendeeUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_attendee_schemas.MeetingAttendeeRetrieve:
    return await update_meeting_attendee_service(db, meeting_attendee_id, attendee)


@router.delete("/{meeting_attendee_id}", status_code=204)
async def delete_meeting_attendee(
    meeting_attendee_id: int, db: AsyncSession = Depends(db.get_db)
):
    return await delete_meeting_attendee_service(db, meeting_attendee_id)


@router.get(
    "/by_meeting/{meeting_id}",
    response_model=List[meeting_attendee_schemas.MeetingAttendeeRetrieve],
)
async def get_attendees_by_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_attendee_schemas.MeetingAttendeeRetrieve]:
    return await get_attendees_by_meeting_service(db, meeting_id)


@router.get(
    "/user_meetings/{user_id}", response_model=List[meeting_schemas.MeetingRetrieve]
)
async def get_meetings_by_user(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[meeting_schemas.MeetingRetrieve]:
    return await get_meetings_by_user_service(db, user_id)
