import sqlalchemy.sql.functions as func
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MeetingRecurrence(Base):
    __tablename__ = "meeting_recurrences"

    id = Column(Integer, primary_key=True)
    frequency = Column(Integer)
    week_day = Column(Integer, nullable=True)
    month_week = Column(Integer, nullable=True)
    interval = Column(Integer, default=1)
    end_recurrence = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    recurrence_id = Column(Integer, ForeignKey("meeting_recurrences.id"), nullable=True)
    title = Column(String(100), default="")
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    duration = Column(Integer, default=30)
    location = Column(String(100), default="")
    notes = Column(String)
    num_reschedules = Column(Integer, default=0)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    recurrence = relationship("MeetingRecurrence", back_populates="meetings")


MeetingRecurrence.meetings = relationship("Meeting", back_populates="recurrence")


class MeetingAttendee(Base):
    __tablename__ = "meeting_attendees"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    user_id = Column(Integer)
    is_scheduler = Column(Boolean, default=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    assignee_id = Column(Integer)
    title = Column(String(100), default="")
    description = Column(String(1000), default="")
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MeetingTask(Base):
    __tablename__ = "meeting_tasks"

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
