from .component import Component
from .task import Task
from typing import Callable, Optional, List

class Node(Component):

    def __init__(self, fn: Callable):
        super().__init__()
        self.fn = fn
        self._has_made_task: List[bool] = []
    
    def _try_get_task(self, index: int) -> Optional[Task]:
        # print("trying to create new task", self.fn.__name__)
        if self._has_made_task[index]:
            # print("already made new task", self._has_made_task)
            return None
        if all(parent.result[index] is not None for parent in self._parents):
            # print("setting has_mate_task = True", self.fn.__name__)
            self._has_made_task[index] = True
            return Task(index, self, *(parent.result[index] for parent in self._parents))
        # else: print("not all true", (parent.result[index] is not None for parent in self._parents))
        return None
    
    def _reset(self, n):
        # print(f"reset with {n}")
        super()._reset(n)
        self._has_made_task = [False for _ in range(n)]
    
    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)
    
    @property
    def __name__(self):
        return self.fn.__name__
    
