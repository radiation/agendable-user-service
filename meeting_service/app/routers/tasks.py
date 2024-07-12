from typing import List

import crud
import db
from fastapi import APIRouter, Depends
from schemas import task_schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[task_schemas.Task])
def read_tasks_by_user(
    user_id: int, db: Session = Depends(db.get_db)
) -> List[task_schemas.Task]:
    return crud.get_tasks_by_user(db, user_id=user_id)


@router.post("/{task_id}/complete", status_code=200)
def complete_task(task_id: int, db: Session = Depends(db.get_db)) -> dict[str, str]:
    crud.mark_task_complete(db, task_id=task_id)
    return {"message": "Task marked as complete"}
