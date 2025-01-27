from typing import List, Callable, Dict, Union, Any, Deque, Optional

from .component import Component
from .node import Node
from .input import Input
from .task import Task
from collections import deque

import itertools

class Pipeline:

    def __init__(self, max_threads: int = 50):
        self._max_threads = max_threads
        self._inputs: Dict[str, Input] = {}
        self._nodes: List[Node] = []

        self._queued_tasks: Deque[Task] = deque()
        self._active_tasks: List[Optional[Task]] = []
        self._num_active_tasks: int = 0

    def node(self, *args):
        def decorator(fn: Callable):
            out = Node(fn)
            out._parents = args
            for component in args:
                component._children.append(out)
            self._nodes.append(out)
            return out
        return decorator
    
    def input(self, name: str) -> Input:
        input = Input(name)
        self._inputs[name] = input
        return input

    def _handle_complete_component(self, component: Component, index: int) -> None:
        for child in component._children:
            if not isinstance(child, Node): continue
            new_task = child._try_get_task(index)
            if new_task is None: continue
            self._queued_tasks.append(new_task)
            self._num_active_tasks += 1
    
    def evaluate(self, inputs: Dict[Union[Input, str], List[Any]]):

        # Basic input validation
        assert set(inputs.keys()) == set(self._inputs.keys()), \
            "keys for values provided must match expected input keys"
        lengths = set(len(value) for value in inputs.values())
        assert len(lengths) == 1, \
            "must provide the same number of values for each input"
        length = lengths.pop()

        # Reset
        self._queued_tasks = deque()
        self._active_tasks = [None] * self._max_threads

        # Setup
        for component in itertools.chain(self._inputs.values(), self._nodes):
            component._reset(length)

        for key, value in inputs.items():
            self._inputs[key].result = value
        
        for component in self._inputs.values():
            for i in range(length):
                self._handle_complete_component(component, i)
        
        # Manage tasks
        while len(self._queued_tasks) + self._num_active_tasks > 0:
            for i, task in enumerate(self._active_tasks):
                if task is None:
                    # Could put another task here
                    if len(self._queued_tasks) > 0:
                        next_task = self._queued_tasks.popleft()
                        self._active_tasks[i] = next_task
                        next_task.start_execute()
                elif task.is_complete:
                    self._active_tasks[i] = None
                    self._num_active_tasks -= 1
                    component: Component = task.node
                    component.result[task.index] = task.result
                    self._handle_complete_component(component, task.index)
        