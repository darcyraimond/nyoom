from time import sleep
from typing import Callable, Any, List, Self

class Node:
    def __init__(self, fn: Callable, pipeline):
        self._fn = fn
        self._pipeline: ParallelPipeline = pipeline
        self._children: List[Self] = []

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


class ParallelPipeline:
    def __init__(self):
        self._roots: List[Callable[[], Any]] = []

    def as_node(self, dependencies: List[Node]):
        def make_node(fn: Callable):
            new_node = Node(fn, self)
            for dep in dependencies:
                dep._children.append(new_node)
            return Node(fn, self)

    # def as_root(self, fn: Callable[[], Any]) -> Node:
    #     self._roots.append(fn)
    #     return Node(fn)


# def double(x: int) -> int:
#     sleep(3)
#     return x * 2


# def square(x: int) -> int:
#     sleep(1)
#     return x * x


# def add(x: int, y: int) -> int:
#     sleep(2)
#     return x + y


if __name__ == "__main__":
    # a = lambda x: x + 1
    # b = lambda x: x + 1
    # c = lambda x: x + 2

    pipeline = ParallelPipeline()

    # @pipeline.as_root
    def double(x: int) -> int:
        sleep(3)
        return x * 2

    # @pipeline.as_root
    def square(x: int) -> int:
        sleep(1)
        return x * x


    def add(x: int, y: int) -> int:
        sleep(2)
        return x + y
    
    print(double)

    # pipeline.add_root()


    # print(a == a)
    # print(a == b)
    # print(a == c)
    # print(add(double(2), square(5)))