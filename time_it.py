from functools import wraps
import datetime
from typing import Any


def timeit(rem: Any = 1):
    def wrapper2(func):
        def wrapper(*args, **kwargs):
            dt = datetime.datetime.now()
            res = func(*args, **kwargs)
            print(f'{rem}time of {func.__name__}: {(datetime.datetime.now() - dt).total_seconds()}')
            return res

        return wrapper

    return wrapper2
