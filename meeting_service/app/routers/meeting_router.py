from app import db
from app.crud import meeting_crud
from app.schemas import meeting_schemas
from app.services import meeting_service
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Helper function to get user metadata from request headers
def get_user_metadata(request: Request) -> dict:
    user_id = request.headers.get("X-User-ID")
    user_email = request.headers.get("X-User-Email")
    if not user_id:
        raise HTTPException(status_code=403, detail="User not authenticated")
    return {"user_id": user_id, "user_email": user_email}


# Create a new meeting
@router.post("/", response_model=meeting_schemas.MeetingRetrieve)
async def create_meeting(
    meeting: meeting_schemas.MeetingCreate, db: AsyncSession = Depends(db.get_db)
) -> meeting_schemas.MeetingRetrieve:
    return await meeting_crud.create_meeting(db=db, meeting=meeting)


# List all meetings
@router.get("/", response_model=list[meeting_schemas.MeetingRetrieve])
async def get_meetings(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[meeting_schemas.MeetingRetrieve]:
    return await meeting_crud.get_meetings(db=db, skip=skip, limit=limit)


# Get a meeting by ID
@router.get("/{meeting_id}", response_model=meeting_schemas.MeetingRetrieve)
async def get_meeting(
    meeting_id: int, request: Request, db: AsyncSession = Depends(db.get_db)
) -> meeting_schemas.MeetingRetrieve:
    # Access the user_id and attendee set by the middleware
    attendee = request.state.attendee

    # Fetch the meeting details
    meeting = await meeting_crud.get_meeting(db=db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Add attendee-specific data (e.g., private notes)
    meeting_data = meeting_schemas.MeetingRetrieve.model_validate(meeting).model_dump()
    meeting_data["private_notes"] = attendee.private_notes

    return meeting_schemas.MeetingRetrieve(**meeting_data)


# Update an existing meeting
@router.put("/{meeting_id}", response_model=meeting_schemas.MeetingRetrieve)
async def update_meeting(
    meeting_id: int,
    meeting: meeting_schemas.MeetingUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    updated_meeting = await meeting_crud.update_meeting(
        db=db, meeting_id=meeting_id, meeting=meeting
    )
    if updated_meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return updated_meeting


# Delete a meeting
@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting(meeting_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await meeting_crud.delete_meeting(db=db, meeting_id=meeting_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meeting not found")


# Complete a meeting and roll tasks over to the next occurrence
@router.post("/{meeting_id}/complete/", response_model=dict)
async def complete_meeting(meeting_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await meeting_crud.complete_meeting(db=db, meeting_id=meeting_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Meeting not found or already completed"
        )
    return {"message": "Meeting completed"}


# Add a recurrence to a meeting
@router.post(
    "/{meeting_id}/add_recurrence/{recurrence_id}",
    response_model=meeting_schemas.MeetingRetrieve,
)
async def add_recurrence(
    meeting_id: int,
    recurrence_id: int,
    db: AsyncSession = Depends(db.get_db),
) -> meeting_schemas.MeetingRetrieve:
    meeting = await meeting_crud.add_recurrence(
        db=db, meeting_id=meeting_id, recurrence_id=recurrence_id
    )
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


# Get the next meeting after a given meeting
@router.get("/{meeting_id}/next/", response_model=meeting_schemas.MeetingRetrieve)
async def next_meeting(
    meeting_id: int, db: AsyncSession = Depends(db.get_db)
) -> meeting_schemas.MeetingRetrieve:
    current_meeting = await meeting_crud.get_meeting(db, meeting_id)
    next_meeting = await meeting_service.get_subsequent_meeting(
        db, current_meeting, after_date=current_meeting.end_date
    )
    if not next_meeting:
        raise HTTPException(status_code=404, detail="Next meeting not found")
    return next_meeting
