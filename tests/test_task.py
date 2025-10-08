import pytest
from uuid import UUID
from app.exceptions import TaskNotFoundError


def test_create_task(storage):
    task_id = storage.create_task(description='test_task')

    assert isinstance(UUID(task_id), UUID)


def test_get_task(storage):
    task_id = storage.create_task(description='test_task')
    task = storage.get_task(task_id)

    assert task['description'] == 'test_task'
    assert task['status'] == 'todo'


def test_get_tasks(storage):
    first_task_id = storage.create_task(description='test_task_1')
    second_task_id = storage.create_task(description='test_task_2')
    storage_tasks = storage.get_tasks()
    task_ids = [task['id'] for task in storage_tasks]

    assert first_task_id in task_ids
    assert second_task_id in task_ids


def test_delete_task(storage):
    task_id = storage.create_task(description='test_task')
    task = storage.get_task(task_id)

    assert task['id'] == task_id

    storage.delete_task(task_id)

    with pytest.raises(TaskNotFoundError) as e:
        storage.get_task(task_id)

    assert str(e.value) == f'Task with id: {task_id} is not found.'


def test_update_task(storage):
    task_id = storage.create_task(description='test_task')
    original_task = storage.get_task(task_id)

    assert original_task['id'] == task_id
    assert original_task['description'] == 'test_task'

    updated_task = storage.update_task(task_id, description='test_task_updated')

    task = storage.get_task(updated_task['id'])

    assert task['id'] == task_id
    assert updated_task['description'] == 'test_task_updated'
