from itertools import count
from random import randint, choices
from string import ascii_letters

from schemas.task import Task


def create_tasks(
    quantity: int = 10,
) -> dict[int, Task]:
    id_generator = count()
    tasks_generator = (
        Task(
            id=next(id_generator),
            name="".join(choices(ascii_letters, k=10)),
            pomodoro_count=randint(1, 11),
            category_id=randint(1, 4),
        )
        for _ in range(quantity)
    )
    return {task.id: task for task in tasks_generator}


tasks = create_tasks()

fake_tasks = lambda: tasks
