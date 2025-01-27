from typing import List, Union, Callable, Dict, Any
from nyoom import Node, Input, Pipeline


pipeline = Pipeline()

# pipeline.input
# x = Input("x")

# pipeline.input
# y = Input("y")

x = pipeline.input("x")
y = pipeline.input("y")

@pipeline.node(x)
def double(x: int) -> int:
    return x * 2

@pipeline.node(y)
def square(x: int) -> int:
    return x * x

@pipeline.node(double, square)
def add(x: int, y: int) -> int:
    return x + y

@pipeline.node(add)
def add_one(x: int) -> int:
    return x + 1

@pipeline.node(add)
def add_two(x: int) -> int:
    return x + 2

pipeline.evaluate({"x": [4, 4, 6], "y": [7, 7, 1]})

print(add_one.result)
print(add_two.result)
print(add_one(2))

"""
double(x) \                  /-> add_one(x)
           |-> add(x, y) ->-|
square(x) /                  \-> add_two(x)
"""
