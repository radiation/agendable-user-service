from datetime import datetime, timedelta

import pytest
from app.models import Meeting
from app.repositories.meeting_repository import MeetingRepository
from app.schemas.meeting_schemas import MeetingCreate, MeetingUpdate
from app.services.meeting_service import (
    create_meeting_service,
    delete_meeting_service,
    get_meeting_service,
    update_meeting_service,
)


@pytest.mark.asyncio
async def test_create_meeting_service(test_client):
    client, db_session = test_client

    new_meeting = MeetingCreate(
        title="Service Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    created_meeting = await create_meeting_service(db_session, new_meeting)
    assert created_meeting.title == "Service Test Meeting"
    assert created_meeting.duration == 60


@pytest.mark.asyncio
async def test_get_meeting_service(test_client):
    client, db_session = test_client

    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    retrieved_meeting = await get_meeting_service(db_session, meeting.id)
    assert retrieved_meeting.title == "Test Meeting"
    assert retrieved_meeting.duration == 60


@pytest.mark.asyncio
async def test_update_meeting_service(test_client):
    client, db_session = test_client

    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    update_data = MeetingUpdate(title="Updated Test Meeting", duration=120)
    updated_meeting = await update_meeting_service(db_session, meeting.id, update_data)
    assert updated_meeting.title == "Updated Test Meeting"
    assert updated_meeting.duration == 120


@pytest.mark.asyncio
async def test_delete_meeting_service(test_client):
    client, db_session = test_client
    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    await delete_meeting_service(db_session, meeting.id)
    deleted = await MeetingRepository(db_session).get_by_id(meeting.id)
    assert deleted is None
