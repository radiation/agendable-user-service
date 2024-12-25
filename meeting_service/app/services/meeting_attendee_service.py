from app.errors import NotFoundError
from app.repositories.meeting_attendee_repository import MeetingAttendeeRepository
from app.schemas.meeting_attendee_schemas import (
    MeetingAttendeeCreate,
    MeetingAttendeeRetrieve,
    MeetingAttendeeUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def create_meeting_attendee_service(
    db: AsyncSession, attendee_data: MeetingAttendeeCreate
) -> MeetingAttendeeRetrieve:
    repo = MeetingAttendeeRepository(db)
    attendee = await repo.create(attendee_data.model_dump())
    return MeetingAttendeeRetrieve.model_validate(attendee)


async def get_meeting_attendees_service(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingAttendeeRetrieve]:
    repo = MeetingAttendeeRepository(db)
    attendees = await repo.get_all(skip=skip, limit=limit)
    return [MeetingAttendeeRetrieve.model_validate(attendee) for attendee in attendees]


async def get_meeting_attendee_service(
    db: AsyncSession, meeting_attendee_id: int
) -> MeetingAttendeeRetrieve:
    repo = MeetingAttendeeRepository(db)
    attendee = await repo.get_by_id(meeting_attendee_id)
    if not attendee:
        raise NotFoundError(
            detail=f"Meeting attendee with ID {meeting_attendee_id} not found"
        )
    return MeetingAttendeeRetrieve.model_validate(attendee)


async def update_meeting_attendee_service(
    db: AsyncSession, meeting_attendee_id: int, update_data: MeetingAttendeeUpdate
) -> MeetingAttendeeRetrieve:
    repo = MeetingAttendeeRepository(db)
    attendee = await repo.update(
        meeting_attendee_id, update_data.model_dump(exclude_unset=True)
    )
    if not attendee:
        raise NotFoundError(
            detail=f"Meeting attendee with ID {meeting_attendee_id} not found"
        )
    return MeetingAttendeeRetrieve.model_validate(attendee)


async def delete_meeting_attendee_service(
    db: AsyncSession, meeting_attendee_id: int
) -> bool:
    repo = MeetingAttendeeRepository(db)
    success = await repo.delete(meeting_attendee_id)
    if not success:
        raise NotFoundError(
            detail=f"Meeting attendee with ID {meeting_attendee_id} not found"
        )
    return success


async def get_attendees_by_meeting_service(
    db: AsyncSession, meeting_id: int
) -> list[MeetingAttendeeRetrieve]:
    repo = MeetingAttendeeRepository(db)
    attendees = await repo.get_attendees_by_meeting(meeting_id)
    return [MeetingAttendeeRetrieve.model_validate(attendee) for attendee in attendees]


async def get_meetings_by_user_service(
    db: AsyncSession, user_id: int
) -> list[MeetingAttendeeRetrieve]:
    repo = MeetingAttendeeRepository(db)
    meetings = await repo.get_meetings_by_user(user_id)
    return [MeetingAttendeeRetrieve.model_validate(meeting) for meeting in meetings]
