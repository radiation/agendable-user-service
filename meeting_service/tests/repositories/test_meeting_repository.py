from datetime import datetime, timedelta

import pytest
from app.models import Meeting
from app.repositories.meeting_repository import MeetingRepository


@pytest.mark.asyncio
async def test_create_meeting(test_client):
    client, db_session = test_client
    repo = MeetingRepository(db_session)

    new_meeting = {
        "title": "Test Meeting",
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(hours=1),
        "duration": 60,
    }
    meeting = await repo.create(new_meeting)
    assert meeting.title == "Test Meeting"
    assert meeting.duration == 60


@pytest.mark.asyncio
async def test_get_meeting_by_id(test_client):
    client, db_session = test_client
    repo = MeetingRepository(db_session)

    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    retrieved = await repo.get_by_id(meeting.id)
    assert retrieved.title == "Test Meeting"
    assert retrieved.duration == 60


@pytest.mark.asyncio
async def test_update_meeting(test_client):
    client, db_session = test_client
    repo = MeetingRepository(db_session)

    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    updated_data = {"title": "Updated Meeting", "duration": 120}
    updated_meeting = await repo.update(meeting.id, updated_data)
    assert updated_meeting.title == "Updated Meeting"
    assert updated_meeting.duration == 120


@pytest.mark.asyncio
async def test_delete_meeting(test_client):
    client, db_session = test_client
    repo = MeetingRepository(db_session)

    meeting = Meeting(
        title="Test Meeting",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(hours=1),
        duration=60,
    )
    db_session.add(meeting)
    await db_session.commit()

    await repo.delete(meeting.id)
    deleted = await repo.get_by_id(meeting.id)
    assert deleted is None
