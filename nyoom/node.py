from .component import Component
from .task import Task
from typing import Callable, Optional, List

class Node(Component):

    def __init__(self, fn: Callable):
        super().__init__()
        self.fn = fn
        self._has_made_task: List[bool] = []
    
    def _try_get_task(self, index: int) -> Optional[Task]:
        # print(f"trying to get task {index} of {len(self._has_made_task)}")
        # print(self._parents)
        # print(self._children)
        if self._has_made_task[index]: return None
        if all(parent.result[index] is not None for parent in self._parents):
            self._has_made_task[index] = True
            return Task(index, self, *(parent.result[index] for parent in self._parents))
        return None
    
    def _reset(self, n):
        # print(f"reset with {n}")
        super()._reset(n)
        self._has_made_task = [False for _ in range(n)]
    
    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)
    
