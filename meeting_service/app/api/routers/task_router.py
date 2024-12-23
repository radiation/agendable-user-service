from typing import List

from app.crud import task_crud
from app.db import db
from app.schemas import task_schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# Create a new task
@router.post("/", response_model=task_schemas.TaskRetrieve)
async def create_task(
    task: task_schemas.TaskCreate, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.TaskRetrieve:
    return await task_crud.create_task(db=db, task=task)


# List all tasks
@router.get("/", response_model=List[task_schemas.TaskRetrieve])
async def get_tasks(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(db.get_db)
) -> list[task_schemas.TaskRetrieve]:
    return await task_crud.get_tasks(db=db, skip=skip, limit=limit)


# Get a task by ID
@router.get("/{task_id}", response_model=task_schemas.TaskRetrieve)
async def get_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.TaskRetrieve:
    task = await task_crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update an existing task
@router.put("/{task_id}", response_model=task_schemas.TaskRetrieve)
async def update_task(
    task_id: int,
    task: task_schemas.TaskUpdate,
    db: AsyncSession = Depends(db.get_db),
) -> task_schemas.TaskRetrieve:
    updated_task = await task_crud.update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


# Delete a task
@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(db.get_db)):
    success = await task_crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")


# Get all tasks for a specific user
@router.get("/user/{user_id}", response_model=List[task_schemas.TaskRetrieve])
async def read_tasks_by_user(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> List[task_schemas.TaskRetrieve]:
    return await task_crud.get_tasks_by_user(db=db, user_id=user_id)


# Mark a task as complete
@router.post("/{task_id}/complete", response_model=task_schemas.TaskRetrieve)
async def complete_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> task_schemas.TaskRetrieve:
    task = await task_crud.mark_task_complete(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="Task not found or already completed"
        )
    return task
