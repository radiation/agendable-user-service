import re

from app.crud.meeting_attendee import get_meeting_attendee
from app.db import get_db
from app.utils import get_user_metadata
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession


async def extract_meeting_id(path: str) -> int:
    # Assuming meeting ID is part of the path, e.g., /meetings/{meeting_id}
    match = re.search(r"/meetings/(\d+)", path)
    if match:
        return int(match.group(1))
    return None


async def meeting_permission_middleware(request: Request, call_next):
    if request.url.path.startswith("/meetings/") and request.method != "POST":
        user_metadata = get_user_metadata(request)
        user_id = user_metadata["user_id"]

        # Attach user_id to the request for downstream access
        request.state.user_id = user_id

        # Extract meeting_id from the path
        meeting_id = await extract_meeting_id(request.url.path)
        if not meeting_id:
            raise HTTPException(status_code=400, detail="Invalid meeting ID in path.")

        # Validate attendee
        db: AsyncSession = await get_db()
        attendee = await get_meeting_attendee(
            db=db, meeting_id=meeting_id, user_id=user_id
        )
        if not attendee:
            raise HTTPException(
                status_code=403, detail="You are not authorized to access this meeting."
            )

        # Attach attendee to the request for downstream access
        request.state.attendee = attendee

    return await call_next(request)
