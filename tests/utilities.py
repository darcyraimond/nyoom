import time
from typing import Callable

def double(x: int, delay: float = 0.0) -> int:
    time.sleep(delay)
    return x * 2

def square(x: int, delay: float = 0.0) -> int:
    time.sleep(delay)
    return x * x

def add(x: int, y: int, delay: float = 0.0) -> int:
    time.sleep(delay)
    return x + y

def add_one(x: int, delay: float = 0.0) -> int:
    time.sleep(delay)
    return x + 1

def add_two(x: int, delay: float = 0.0) -> int:
    time.sleep(delay)
    return x + 2

def impose_time_limit(*, lower_limit: float = 0.0, upper_limit: float = float("inf")) -> Callable:
    def decorator(fn: Callable) -> Callable:
        def out():
            start_time = time.time()
            fn()
            end_time = time.time()
            time_taken = end_time - start_time
            assert time_taken <= upper_limit, f"upper limit exceeded ({time_taken} > {upper_limit})"
            assert time_taken >= lower_limit, f"lower limit not met ({time_taken} < {lower_limit})"
        return out
    return decorator