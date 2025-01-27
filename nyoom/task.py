from typing import Callable, Optional, Any

class Task:
    def __init__(self, index: int, node: Callable, *args):
        self.index = index
        self.node = node
        self.args = args
        self.result: Optional[Any] = None
        self.is_complete = False
    
    def start_execute(self):
        # TODO make this parallel
        self.result = self.node(*self.args)
        self.is_complete = True
    
    def join(self):
        # TODO block until execution is complete
        # shouldn't be called under normal operation
        pass
    
    def kill(self):
        # TODO kill task without raising exception
        # shouldn't be called under normal operation
        pass