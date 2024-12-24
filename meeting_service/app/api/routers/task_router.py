from app.db import db
from app.schemas.task_schemas import TaskCreate, TaskRetrieve, TaskUpdate
from app.services.task_service import (
    create_task_service,
    delete_task_service,
    get_task_service,
    get_tasks_by_user_service,
    mark_task_complete_service,
    update_task_service,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=TaskRetrieve)
async def create_task(
    task: TaskCreate, db: AsyncSession = Depends(db.get_db)
) -> TaskRetrieve:
    return await create_task_service(db, task)


@router.get("/", response_model=list[TaskRetrieve])
async def get_tasks(db: AsyncSession = Depends(db.get_db)) -> list[TaskRetrieve]:
    return await get_tasks_by_user_service(db, user_id=None)


@router.get("/{task_id}", response_model=TaskRetrieve)
async def get_task(task_id: int, db: AsyncSession = Depends(db.get_db)) -> TaskRetrieve:
    return await get_task_service(db, task_id)


@router.put("/{task_id}", response_model=TaskRetrieve)
async def update_task(
    task_id: int, task: TaskUpdate, db: AsyncSession = Depends(db.get_db)
) -> TaskRetrieve:
    return await update_task_service(db, task_id, task)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(db.get_db)):
    return await delete_task_service(db, task_id)


@router.get("/user/{user_id}", response_model=list[TaskRetrieve])
async def get_tasks_by_user(
    user_id: int, db: AsyncSession = Depends(db.get_db)
) -> list[TaskRetrieve]:
    return await get_tasks_by_user_service(db, user_id)


@router.post("/{task_id}/complete", response_model=TaskRetrieve)
async def complete_task(
    task_id: int, db: AsyncSession = Depends(db.get_db)
) -> TaskRetrieve:
    return await mark_task_complete_service(db, task_id)
