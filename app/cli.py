import argparse
from storage import JSONStorage, Status
from exceptions import *

todo_list = JSONStorage('storage.json')


def add_task(args):
    """Add task from todo_list"""
    task_id = todo_list.create_task(args.description)
    print(f"Task with id: {task_id} added successfully!")


def show_tasks(args):
    """Show list of tasks from todo_list"""
    tasks = todo_list.get_tasks()
    print(
        '\n'.join([f"{t['id']}: {t['description']} - {t['status']}" for t in tasks]),
        sep='\n',
    )


def show_task(args):
    """Show task from todo_list"""
    try:
        task = todo_list.get_task(args.id)
        print(f'Task: f{task}')
    except TaskNotFoundError as e:
        print(e)


def complete_task(args):
    """Complete task from todo_list"""
    try:
        task = todo_list.get_task(args.id)
        if task['status'] == Status.DONE.value:
            raise ValueError('Task is already completed.')
        todo_list.update_task(args.id, status=Status.DONE.value)
        print(f"Task with id: {args.id} completed successfully!")
    except TaskNotFoundError as e:
        print(e)
    except TaskError as e:
        print(e)
    except Exception as e:
        print(e)


def delete_task(args):
    """Delete task from todo_list"""
    try:
        deleted_task = todo_list.delete_task(args.id)
        if deleted_task:
            print(f"Task {args.id} deleted.")
        else:
            print("Invalid task id.")
    except TaskNotFoundError as err:
        print(err)


def clear_todo_list(args):
    """Clear todo_list"""
    todo_list.delete_tasks()
    print("All tasks removed.")


def update_task(args):
    todo_list.update_task(args.id, description=args.description)
    print(f"Task with id: {args.id} updated successfully!")


def update_status(args):
    try:
        todo_list.update_task(args.id, status=args.status)
        print(f"Task with id: {args.id} updated successfully!")
    except TaskError as e:
        print(e)


def main():
    parser = argparse.ArgumentParser(description="ToDo List CLI")
    subparsers = parser.add_subparsers()

    # add task
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Task description")
    parser_add.set_defaults(func=add_task)

    # update task
    parser_add = subparsers.add_parser("update", help="Update a task by ID")
    parser_add.add_argument("id", type=str, help="Task ID")
    parser_add.add_argument("description", type=str, help="Task description")
    parser_add.set_defaults(func=update_task)

    # update status
    parser_add = subparsers.add_parser(
        "update_status", help="Update a task status by ID"
    )
    parser_add.add_argument("id", type=str, help="Task ID")
    parser_add.add_argument("status", type=str, help="Task status")
    parser_add.set_defaults(func=update_status)

    # show all tasks
    parser_show_all = subparsers.add_parser("show_all", help="Show all tasks")
    parser_show_all.set_defaults(func=show_tasks)

    # show one task
    parser_show = subparsers.add_parser("show", help="Show task by ID")
    parser_show.add_argument("id", type=str, help="Task ID")
    parser_show.set_defaults(func=show_task)

    # complete task
    parser_complete = subparsers.add_parser("complete", help="Mark task as done by ID")
    parser_complete.add_argument("id", type=str, help="Task ID")
    parser_complete.set_defaults(func=complete_task)

    # delete task
    parser_delete = subparsers.add_parser("delete", help="Delete task by ID")
    parser_delete.add_argument("id", type=str, help="Task ID")
    parser_delete.set_defaults(func=delete_task)

    # clear completed tasks
    parser_clear = subparsers.add_parser("clear", help="Remove all completed tasks")
    parser_clear.set_defaults(func=clear_todo_list)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
