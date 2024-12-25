from datetime import datetime

from app.errors import NotFoundError
from app.repositories.meeting_recurrence_repository import MeetingRecurrenceRepository
from app.schemas import meeting_recurrence_schemas
from dateutil.rrule import rrulestr
from sqlalchemy.ext.asyncio import AsyncSession


async def create_recurrence_service(
    db: AsyncSession,
    recurrence_data: meeting_recurrence_schemas.MeetingRecurrenceCreate,
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    repo = MeetingRecurrenceRepository(db)
    recurrence = await repo.create(recurrence_data.model_dump())
    return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
        recurrence
    )


async def get_recurrence_service(
    db: AsyncSession, recurrence_id: int
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    repo = MeetingRecurrenceRepository(db)
    recurrence = await repo.get_by_id(recurrence_id)
    if not recurrence:
        raise NotFoundError(detail="Recurrence with ID {recurrence_id} not found")
    return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
        recurrence
    )


async def update_recurrence_service(
    db: AsyncSession,
    recurrence_id: int,
    recurrence_data: meeting_recurrence_schemas.MeetingRecurrenceUpdate,
) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
    repo = MeetingRecurrenceRepository(db)
    recurrence = await repo.get_by_id(recurrence_id)
    if not recurrence:
        raise NotFoundError(detail="Recurrence with ID {recurrence_id} not found")

    for key, value in recurrence_data.model_dump(exclude_unset=True).items():
        setattr(recurrence, key, value)

    await db.commit()
    await db.refresh(recurrence)
    return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
        recurrence
    )


async def delete_recurrence_service(db: AsyncSession, recurrence_id: int) -> bool:
    repo = MeetingRecurrenceRepository(db)
    recurrence = await repo.get_by_id(recurrence_id)
    if not recurrence:
        raise NotFoundError(detail="Recurrence with ID {recurrence_id} not found")

    await repo.delete(recurrence_id)
    return True


async def get_next_meeting_date(
    db: AsyncSession, recurrence_id: int, after_date: datetime = datetime.now()
) -> datetime:
    repo = MeetingRecurrenceRepository(db)
    recurrence = await repo.get_by_id(recurrence_id)
    if not recurrence:
        return None

    # Parse the rrule string into an rrule object
    rule = rrulestr(recurrence.rrule, dtstart=after_date)

    # Fetch the next occurrence
    try:
        next_meeting_date = list(rule[:1])[0]
        return next_meeting_date
    except StopIteration:
        # Handle the case where no next date is available
        return None
