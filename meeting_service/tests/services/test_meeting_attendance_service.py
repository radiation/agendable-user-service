import pytest
from app.errors import NotFoundError
from app.models import MeetingAttendee
from app.schemas.meeting_attendee_schemas import (
    MeetingAttendeeCreate,
    MeetingAttendeeUpdate,
)
from app.services.meeting_attendee_service import (
    create_meeting_attendee_service,
    delete_meeting_attendee_service,
    get_attendees_by_meeting_service,
    get_meeting_attendee_service,
    get_meetings_by_user_service,
    update_meeting_attendee_service,
)


@pytest.mark.asyncio
async def test_create_meeting_attendee_service(test_client):
    client, db_session = test_client
    new_attendee = MeetingAttendeeCreate(meeting_id=1, user_id=1, is_scheduler=True)
    created_attendee = await create_meeting_attendee_service(db_session, new_attendee)
    assert created_attendee.meeting_id == 1
    assert created_attendee.user_id == 1
    assert created_attendee.is_scheduler is True


@pytest.mark.asyncio
async def test_get_meeting_attendee_service(test_client):
    client, db_session = test_client
    attendee = MeetingAttendee(meeting_id=1, user_id=2, is_scheduler=False)
    db_session.add(attendee)
    await db_session.commit()

    retrieved_attendee = await get_meeting_attendee_service(db_session, attendee.id)
    assert retrieved_attendee.id == attendee.id
    assert retrieved_attendee.user_id == 2
    assert retrieved_attendee.is_scheduler is False


@pytest.mark.asyncio
async def test_update_meeting_attendee_service(test_client):
    client, db_session = test_client
    attendee = MeetingAttendee(meeting_id=1, user_id=3, is_scheduler=False)
    db_session.add(attendee)
    await db_session.commit()

    update_data = MeetingAttendeeUpdate(is_scheduler=True)
    updated_attendee = await update_meeting_attendee_service(
        db_session, attendee.id, update_data
    )
    assert updated_attendee.is_scheduler is True


@pytest.mark.asyncio
async def test_delete_meeting_attendee_service(test_client):
    client, db_session = test_client
    attendee = MeetingAttendee(meeting_id=1, user_id=4, is_scheduler=False)
    db_session.add(attendee)
    await db_session.commit()

    # Delete the attendee
    await delete_meeting_attendee_service(db_session, attendee.id)

    # Verify the attendee no longer exists
    with pytest.raises(NotFoundError) as exc_info:
        await get_meeting_attendee_service(db_session, attendee.id)

    # Assert the correct error message
    assert exc_info.value.detail == f"Meeting attendee with ID {attendee.id} not found"


@pytest.mark.asyncio
async def test_get_attendees_by_meeting_service(test_client):
    client, db_session = test_client
    attendee1 = MeetingAttendee(meeting_id=1, user_id=5, is_scheduler=False)
    attendee2 = MeetingAttendee(meeting_id=1, user_id=6, is_scheduler=True)
    db_session.add_all([attendee1, attendee2])
    await db_session.commit()

    attendees = await get_attendees_by_meeting_service(db_session, meeting_id=1)
    assert len(attendees) == 2


@pytest.mark.asyncio
async def test_get_meetings_by_user_service(test_client):
    client, db_session = test_client
    attendee1 = MeetingAttendee(meeting_id=2, user_id=7, is_scheduler=False)
    attendee2 = MeetingAttendee(meeting_id=3, user_id=7, is_scheduler=True)
    db_session.add_all([attendee1, attendee2])
    await db_session.commit()

    meetings = await get_meetings_by_user_service(db_session, user_id=7)
    assert len(meetings) == 2
