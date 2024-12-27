from datetime import datetime

from app.errors import NotFoundError
from app.repositories.meeting_recurrence_repository import MeetingRecurrenceRepository
from app.schemas import meeting_recurrence_schemas
from dateutil.rrule import rrulestr


class MeetingRecurrenceService:
    def __init__(self, recurrence_repo: MeetingRecurrenceRepository):
        self.recurrence_repo = recurrence_repo

    async def create_recurrence(
        self, recurrence_data: meeting_recurrence_schemas.MeetingRecurrenceCreate
    ) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
        recurrence = await self.recurrence_repo.create(recurrence_data.model_dump())
        return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
            recurrence
        )

    async def get_recurrence(
        self, recurrence_id: int
    ) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
        recurrence = await self.recurrence_repo.get_by_id(recurrence_id)
        if not recurrence:
            raise NotFoundError(detail=f"Recurrence with ID {recurrence_id} not found")
        return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
            recurrence
        )

    async def update_recurrence(
        self,
        recurrence_id: int,
        recurrence_data: meeting_recurrence_schemas.MeetingRecurrenceUpdate,
    ) -> meeting_recurrence_schemas.MeetingRecurrenceRetrieve:
        recurrence = await self.recurrence_repo.get_by_id(recurrence_id)
        if not recurrence:
            raise NotFoundError(detail=f"Recurrence with ID {recurrence_id} not found")

        for key, value in recurrence_data.model_dump(exclude_unset=True).items():
            setattr(recurrence, key, value)

        await self.recurrence_repo.db.commit()
        await self.recurrence_repo.db.refresh(recurrence)
        return meeting_recurrence_schemas.MeetingRecurrenceRetrieve.model_validate(
            recurrence
        )

    async def delete_recurrence(self, recurrence_id: int) -> bool:
        recurrence = await self.recurrence_repo.get_by_id(recurrence_id)
        if not recurrence:
            raise NotFoundError(detail=f"Recurrence with ID {recurrence_id} not found")

        await self.recurrence_repo.delete(recurrence_id)
        return True

    async def get_next_meeting_date(
        self, recurrence_id: int, after_date: datetime = datetime.now()
    ) -> datetime:
        recurrence = await self.recurrence_repo.get_by_id(recurrence_id)
        if not recurrence:
            return None

        rule = rrulestr(recurrence.rrule, dtstart=after_date)
        try:
            next_meeting_date = list(rule[:1])[0]
            return next_meeting_date
        except StopIteration:
            return None
