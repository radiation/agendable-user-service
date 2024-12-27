from datetime import datetime

from app.errors import NotFoundError, ValidationError
from app.models import Meeting, MeetingRecurrence
from app.repositories.meeting_attendee_repository import MeetingAttendeeRepository
from app.repositories.meeting_repository import MeetingRepository
from app.schemas import meeting_schemas
from dateutil.rrule import rrulestr


class MeetingService:
    def __init__(
        self, meeting_repo: MeetingRepository, attendee_repo: MeetingAttendeeRepository
    ):
        self.meeting_repo = meeting_repo
        self.attendee_repo = attendee_repo

    async def create_meeting(
        self, meeting_data: meeting_schemas.MeetingCreate
    ) -> meeting_schemas.MeetingRetrieve:
        if meeting_data.recurrence_id:
            recurrence = await self.meeting_repo.db.get(
                MeetingRecurrence, meeting_data.recurrence_id
            )
            if not recurrence:
                raise ValidationError(
                    detail=f"Recurrence with ID {meeting_data.recurrence_id} not found"
                )

        meeting = await self.meeting_repo.create_with_recurrence(
            meeting_data.model_dump()
        )
        return meeting_schemas.MeetingRetrieve.model_validate(meeting)

    async def list_meetings(
        self, skip: int = 0, limit: int = 10
    ) -> list[meeting_schemas.MeetingRetrieve]:
        meetings = await self.meeting_repo.get_all(skip=skip, limit=limit)
        return [
            meeting_schemas.MeetingRetrieve.model_validate(meeting)
            for meeting in meetings
        ]

    async def get_meeting(self, meeting_id: int) -> meeting_schemas.MeetingRetrieve:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")
        return meeting_schemas.MeetingRetrieve.model_validate(meeting)

    async def update_meeting(
        self, meeting_id: int, meeting_data: meeting_schemas.MeetingUpdate
    ) -> meeting_schemas.MeetingRetrieve:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

        for key, value in meeting_data.model_dump(exclude_unset=True).items():
            setattr(meeting, key, value)

        await self.meeting_repo.db.commit()
        await self.meeting_repo.db.refresh(meeting)
        return meeting_schemas.MeetingRetrieve.model_validate(meeting)

    async def delete_meeting(self, meeting_id: int) -> bool:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            return False
        await self.meeting_repo.delete(meeting_id)
        return True

    async def complete_meeting(
        self, meeting_id: int
    ) -> meeting_schemas.MeetingRetrieve:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

        meeting.completed = True
        await self.meeting_repo.db.commit()
        await self.meeting_repo.db.refresh(meeting)
        return meeting_schemas.MeetingRetrieve.model_validate(meeting)

    async def add_recurrence(
        self, meeting_id: int, recurrence_id: int
    ) -> meeting_schemas.MeetingRetrieve:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

        meeting.recurrence_id = recurrence_id
        await self.meeting_repo.db.commit()
        await self.meeting_repo.db.refresh(meeting)
        return meeting_schemas.MeetingRetrieve.model_validate(meeting)

    async def get_subsequent_meeting(
        self, meeting_id: int, after_date: datetime = datetime.now()
    ) -> meeting_schemas.MeetingRetrieve:
        meeting = await self.meeting_repo.get_by_id_with_recurrence(meeting_id)
        if not meeting:
            raise NotFoundError(detail=f"Meeting with ID {meeting_id} not found")

        if not meeting.recurrence_id:
            raise ValidationError(
                detail=f"Meeting {meeting_id} does not have a recurrence set"
            )

        recurrence = await self.meeting_repo.db.get(
            MeetingRecurrence, meeting.recurrence_id
        )
        if not recurrence:
            raise NotFoundError(
                detail=f"Recurrence with ID {meeting.recurrence_id} not found"
            )

        next_meeting = await self.meeting_repo.get_meetings_with_recurrence(
            recurrence_id=meeting.recurrence_id, after_date=after_date
        )

        if not next_meeting:
            next_meeting = await self.create_subsequent_meeting(meeting)
        else:
            next_meeting = next_meeting[0]

        return meeting_schemas.MeetingRetrieve.model_validate(next_meeting)

    async def create_subsequent_meeting(
        self, meeting: Meeting
    ) -> meeting_schemas.MeetingRetrieve:
        if not meeting:
            raise NotFoundError(detail="Meeting not found")

        if not meeting.recurrence_id:
            raise ValidationError(
                detail=f"Meeting with ID {meeting.id} does not have a recurrence set"
            )

        recurrence = await self.meeting_repo.db.get(
            MeetingRecurrence, meeting.recurrence_id
        )
        if not recurrence:
            raise NotFoundError(
                detail=f"Recurrence with ID {meeting.recurrence_id} not found"
            )

        try:
            rule = rrulestr(recurrence.rrule, dtstart=meeting.start_date)
            next_meeting_date = rule.after(meeting.start_date, inc=False)
        except Exception as e:
            raise ValidationError(detail=f"Error parsing recurrence rule: {str(e)}")

        if not next_meeting_date:
            raise ValidationError(detail="No future dates found in the recurrence rule")

        duration = meeting.end_date - meeting.start_date if meeting.end_date else None
        next_meeting_end_date = next_meeting_date + duration if duration else None

        meeting_data = meeting_schemas.MeetingCreate(
            title=meeting.title,
            start_date=next_meeting_date,
            end_date=next_meeting_end_date,
            duration=meeting.duration,
            location=meeting.location,
            notes=meeting.notes,
            recurrence_id=meeting.recurrence_id,
        )

        new_meeting = await self.meeting_repo.create(meeting_data.model_dump())
        return meeting_schemas.MeetingRetrieve.model_validate(new_meeting)

    async def create_meeting_with_recurrence_and_attendees(
        self, meeting_data: dict, attendees: list[dict]
    ):
        async with self.meeting_repo.db.begin():
            meeting = await self.meeting_repo.create_with_recurrence(meeting_data)

            for attendee_data in attendees:
                attendee_data["meeting_id"] = meeting.id
                await self.attendee_repo.create(attendee_data)

            return meeting

    async def create_recurring_meetings(
        self, recurrence_id: int, base_meeting: dict, dates: list[datetime]
    ):
        recurrence = await self.meeting_repo.db.get(MeetingRecurrence, recurrence_id)
        if not recurrence:
            raise NotFoundError(detail=f"Recurrence with ID {recurrence_id} not found")

        meetings = await self.meeting_repo.batch_create_with_recurrence(
            recurrence_id, base_meeting, dates
        )
        return [meeting.model_dump() for meeting in meetings]
