import pytest
from app.errors import NotFoundError
from app.models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate


@pytest.mark.asyncio
async def test_create_task(task_service):
    new_task = TaskCreate(title="New Task", assignee_id=1)
    created_task = await task_service.create_task(new_task)

    assert created_task.title == "New Task"


@pytest.mark.asyncio
async def test_get_task_by_id(task_service):
    task = Task(title="Task 1")
    created_task = await task_service.create_task(
        TaskCreate(title=task.title, assignee_id=1)
    )

    retrieved_task = await task_service.get_task(created_task.id)
    assert retrieved_task.title == "Task 1"


@pytest.mark.asyncio
async def test_update_task(task_service, db_session):
    new_task = TaskCreate(title="New Task", assignee_id=1)
    created_task = await task_service.create_task(new_task)

    update_data = TaskUpdate(title="Updated Task")
    updated_task = await task_service.update_task(created_task.id, update_data)

    assert updated_task.title == "Updated Task"


@pytest.mark.asyncio
async def test_delete_task(task_service, db_session):
    task = Task(title="Task 1")
    db_session.add(task)
    await db_session.commit()

    await task_service.delete_task(task.id)

    # Verify that the task is deleted
    with pytest.raises(NotFoundError):
        await task_service.get_task(task.id)


@pytest.mark.asyncio
async def test_get_tasks_by_user(task_service, db_session):
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")

    db_session.add_all([task1, task2])
    await db_session.commit()

    tasks = await task_service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
