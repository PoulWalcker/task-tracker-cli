import json
import pathlib
from app.utils import open_json
from uuid import uuid4
from enum import Enum
from app.exceptions import *


class Status(Enum):
    TODO = 'todo'
    WIP = 'wip'
    DONE = 'done'


class JSONStorage:
    def __init__(self, filename):
        self.filepath = self._init_storage(filename)

    def _init_storage(self, filename):
        p = pathlib.Path(filename)
        if not filename.endswith('.json'):
            raise FileError('Storage must be in .json format only.')
        if not p.exists():
            with p.open('w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        return p

    def create_task(self, description: str):
        with open_json(self.filepath) as tasks:
            task_id = str(uuid4())
            task = {
                'id': task_id,
                'description': description,
                'status': Status.TODO.value,
            }
            tasks[task_id] = task
            return task_id

    def delete_task(self, task_id):
        with open_json(self.filepath) as tasks:
            task = tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(f'Task with id: {task_id} is not found.')
            del tasks[task_id]
            return True

    def delete_tasks(self):
        with open_json(self.filepath) as tasks:
            tasks.clear()
            return True

    def update_task(self, task_id, **ktaskargs):
        with open_json(self.filepath) as tasks:
            task = tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(f'Task with id: {task_id} is not found.')

            if 'status' in ktaskargs:
                st = ktaskargs['status']
                if isinstance(st, Status):
                    ktaskargs['status'] = st.value
                elif st not in {s.value for s in Status}:
                    raise TaskError(f'Invalid status: {st}')

            for k, v in ktaskargs.items():
                if k in task:
                    task[k] = v
            return task

    def get_task(self, task_id):
        with open_json(self.filepath) as tasks:
            task = tasks.get(task_id)
            if task is None:
                raise TaskNotFoundError(f'Task with id: {task_id} is not found.')
            return task

    def get_tasks(self):
        with open_json(self.filepath) as tasks:
            return [v for _, v in tasks.items()]
