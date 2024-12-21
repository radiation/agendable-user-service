from app.models import Meeting, MeetingAttendee, MeetingRecurrence
from app.schemas.meeting_schemas import MeetingCreate, MeetingUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


async def create_meeting(db: AsyncSession, meeting: MeetingCreate) -> Meeting:
    db_meeting = Meeting(**meeting.model_dump())
    db.add(db_meeting)
    await db.commit()
    await db.refresh(db_meeting)

    if db_meeting.recurrence_id:
        db_meeting = await db.execute(
            select(Meeting)
            .options(joinedload(Meeting.recurrence))
            .filter(Meeting.id == db_meeting.id)
        )
        db_meeting = db_meeting.scalars().first()
    return db_meeting


async def get_meetings(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[Meeting]:
    stmt = (
        select(Meeting)
        .options(joinedload(Meeting.recurrence))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    meetings = result.scalars().all()
    return meetings


async def get_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    stmt = (
        select(Meeting)
        .options(joinedload(Meeting.recurrence))
        .filter(Meeting.id == meeting_id)
    )
    result = await db.execute(stmt)
    meeting = result.scalars().first()
    return meeting


async def update_meeting(
    db: AsyncSession, meeting_id: int, meeting: MeetingUpdate
) -> Meeting:
    db_meeting = await get_meeting(db, meeting_id)
    if db_meeting:
        for key, value in meeting.model_dump(exclude_unset=True).items():
            setattr(db_meeting, key, value)
        await db.commit()
        await db.refresh(db_meeting)
    return db_meeting


async def delete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    db_meeting = await get_meeting(db, meeting_id)
    if db_meeting:
        try:
            await db.delete(db_meeting)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return db_meeting
    else:
        return None


async def get_meeting_with_attendee(
    db: AsyncSession, meeting_id: int, user_id: int
) -> Meeting:
    stmt = (
        select(Meeting)
        .options(joinedload(Meeting.attendees))
        .filter(
            Meeting.id == meeting_id,
            Meeting.attendees.any(MeetingAttendee.user_id == user_id),
        )
    )
    result = await db.execute(stmt)
    meeting = result.scalars().first()
    return meeting


async def get_meeting_recurrence_by_meeting(
    db: AsyncSession, meeting_id: int
) -> MeetingRecurrence:
    stmt = select(MeetingRecurrence).filter(MeetingRecurrence.meeting_id == meeting_id)
    result = await db.execute(stmt)
    recurrence = result.scalars().first()
    return recurrence


async def complete_meeting(db: AsyncSession, meeting_id: int) -> Meeting:
    meeting = await get_meeting(db, meeting_id)
    if meeting:
        meeting.completed = True
        await db.commit()
        await db.refresh(meeting)
        return meeting


async def add_recurrence(
    db: AsyncSession, meeting_id: int, recurrence_id: int
) -> Meeting:
    meeting = await get_meeting(db, meeting_id)
    if not meeting:
        raise ValueError("Meeting not found")

    if meeting.recurrence_id is not None:
        # If we're changing the recurrence, we should just update the meeting
        return meeting

    stmt = select(MeetingRecurrence.id).filter(MeetingRecurrence.id == recurrence_id)
    recurrence_exists = await db.scalar(stmt)

    if not recurrence_exists:
        raise ValueError("Recurrence not found")

    meeting.recurrence_id = recurrence_id
    await db.commit()
    await db.refresh(meeting)
    return meeting
