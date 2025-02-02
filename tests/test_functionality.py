from nyoom import Pipeline
from utilities import double, square, add, add_one, add_two, impose_time_limit


@impose_time_limit(upper_limit=0.1)
def test_decorator_syntax():
    pipeline = Pipeline()

    x = pipeline.input("x")
    y = pipeline.input("y")

    @pipeline.node(x)
    def node_1a(x: int) -> int:
        return double(x)
    
    @pipeline.node(y)
    def node_1b(x: int) -> int:
        return square(x)
    
    @pipeline.node(node_1a, node_1b)
    def node_2(x: int, y: int) -> int:
        return add(x, y)

    @pipeline.node(node_2)
    def node_3a(x: int) -> int:
        return add_one(x)

    @pipeline.node(node_2)
    def node_3b(x: int) -> int:
        return add_two(x)

    pipeline.evaluate({"x": [4, 4, 6], "y": [7, 7, 1]})

    assert node_1a.result == [8, 8, 12]
    assert node_1b.result == [49, 49, 1]
    assert node_2.result == [57, 57, 13]
    assert node_3a.result == [58, 58, 14]
    assert node_3b.result == [59, 59, 15]
    

@impose_time_limit(upper_limit=0.1)
def test_functional_syntax():
    pipeline = Pipeline()

    x = pipeline.input("x")
    y = pipeline.input("y")

    node_1a = pipeline.node(x)(double)    
    node_1b = pipeline.node(y)(square)
    node_2 = pipeline.node(node_1a, node_1b)(add)
    node_3a = pipeline.node(node_2)(add_one)
    node_3b = pipeline.node(node_2)(add_two)

    pipeline.evaluate({"x": [4, 4, 6], "y": [7, 7, 1]})

    assert node_1a.result == [8, 8, 12]
    assert node_1b.result == [49, 49, 1]
    assert node_2.result == [57, 57, 13]
    assert node_3a.result == [58, 58, 14]
    assert node_3b.result == [59, 59, 15]