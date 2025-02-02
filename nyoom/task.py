import multiprocessing_on_dill as multiprocessing
from typing import Callable, Optional, Any
from multiprocessing_on_dill import Process, Pipe
from multiprocessing_on_dill.connection import Connection


def _run_func(fn: Callable, args: tuple, sender: Connection):
    result = fn(*args)
    sender.send(result)


class Task:
    def __init__(self, index: int, node: Callable, *args):
        self.index = index
        self.node = node
        self.args = args
        self.is_complete = False
        self.process: Optional[Process] = None
        self.receiver: Optional[Connection] = None
    
    def start_execute(self):
        sender, self.receiver = Pipe()
        self.process = Process(target=_run_func, args=(self.node, self.args, sender))
        self.process.start()
    
    def try_join(self) -> bool:

        if not self.is_complete:
            self.is_complete = self.process.exitcode is not None
        if self.is_complete:
            if self.node.result[self.index] is None:
                result = self.receiver.recv()
                self.node.result[self.index] = result
        return self.is_complete