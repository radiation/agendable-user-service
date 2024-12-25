import sqlalchemy.sql.functions as func
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer

from . import Base


class MeetingTask(Base):
    __tablename__ = "meeting_tasks"
    __table_args__ = (
        Index("ix_meeting_task_meeting_id", "meeting_id"),
        Index("ix_meeting_task_task_id", "task_id"),
    )

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
