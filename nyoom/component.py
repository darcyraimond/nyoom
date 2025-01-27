from abc import ABC, abstractmethod
from typing import List, Any, Optional, Union

class Component(ABC):

    def __init__(self):
        self.result: List[Optional[Any]] = []
        self._parents: List[Component] = []
        self._children: List[Component] = []
    
    def _reset(self, n: int):
        self.result = [None for _ in range(n)]
        
