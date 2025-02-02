from nyoom import Pipeline
from utilities import double, square, add, add_one, add_two, impose_time_limit
import time

@impose_time_limit(upper_limit=1.5)
def test_single():
    pipeline = Pipeline()

    x = pipeline.input("x")

    double_node = pipeline.node(x)(lambda x: double(x, delay=1.0))
    square_node = pipeline.node(x)(lambda x: square(x, delay=1.0))

    pipeline.evaluate({"x": [5]})
    assert double_node.result == [10]
    assert square_node.result == [25]


@impose_time_limit(lower_limit=1.5, upper_limit=2.5)
def test_single_slow():
    pipeline = Pipeline(max_threads=1)

    x = pipeline.input("x")

    double_node = pipeline.node(x)(lambda x: double(x, delay=1.0))
    square_node = pipeline.node(x)(lambda x: square(x, delay=1.0))

    pipeline.evaluate({"x": [5]})
    assert double_node.result == [10]
    assert square_node.result == [25]

