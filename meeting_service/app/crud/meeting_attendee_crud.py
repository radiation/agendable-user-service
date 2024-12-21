from app.models import MeetingAttendee
from app.schemas.meeting_attendee_schemas import (
    MeetingAttendeeCreate,
    MeetingAttendeeUpdate,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def create_meeting_attendee(
    db: AsyncSession, attendee: MeetingAttendeeCreate
) -> MeetingAttendee:
    db_attendee = MeetingAttendee(**attendee.model_dump())
    db.add(db_attendee)
    await db.commit()
    await db.refresh(db_attendee)
    return db_attendee


async def get_meeting_attendees(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[MeetingAttendee]:
    stmt = select(MeetingAttendee).offset(skip).limit(limit)
    result = await db.execute(stmt)
    attendees = result.scalars().all()
    return attendees


# Option to get meeting attendee by ID or by meeting ID and user ID
async def get_meeting_attendee(
    db: AsyncSession,
    meeting_attendee_id: int = None,
    meeting_id: int = None,
    user_id: int = None,
) -> MeetingAttendee:
    if meeting_attendee_id:
        stmt = select(MeetingAttendee).filter(MeetingAttendee.id == meeting_attendee_id)
    elif meeting_id and user_id:
        stmt = select(MeetingAttendee).filter(
            MeetingAttendee.meeting_id == meeting_id, MeetingAttendee.user_id == user_id
        )
    else:
        raise ValueError(
            "You must provide either meeting_attendee_id \
            or both meeting_id and user_id."
        )

    result = await db.execute(stmt)
    attendee = result.scalars().first()
    return attendee


async def update_meeting_attendee(
    db: AsyncSession,
    meeting_attendee_id: int,
    meeting_attendee: MeetingAttendeeUpdate,
) -> MeetingAttendee:
    db_attendee = await get_meeting_attendee(db, meeting_attendee_id)
    if db_attendee:
        for key, value in meeting_attendee.model_dump(exclude_unset=True).items():
            setattr(db_attendee, key, value)
        await db.commit()
        await db.refresh(db_attendee)
    return db_attendee


async def delete_meeting_attendee(
    db: AsyncSession, meeting_attendee_id: int
) -> MeetingAttendee:
    db_meeting_attendee = await get_meeting_attendee(db, meeting_attendee_id)
    if db_meeting_attendee:
        try:
            await db.delete(db_meeting_attendee)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_meeting_attendee
    else:
        return None


async def get_attendees_by_meeting(
    db: AsyncSession, meeting_id: int
) -> list[MeetingAttendee]:
    stmt = select(MeetingAttendee).filter(MeetingAttendee.meeting_id == meeting_id)
    result = await db.execute(stmt)
    attendees = result.scalars().all()
    return attendees


async def get_meetings_by_user(db: AsyncSession, user_id: int) -> list[MeetingAttendee]:
    stmt = select(MeetingAttendee).filter(MeetingAttendee.user_id == user_id)
    result = await db.execute(stmt)
    meetings = result.scalars().all()
    return meetings
