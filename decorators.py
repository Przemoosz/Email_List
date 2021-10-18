import functools
import time

'''
Creator: Przemysław Szewczak
Version: 1.0.2
Update date: 17.10.2021
Python: 3.9.7
It is decorator file nothing interesting here.
You should not change anything here!
'''


def func_timer(_func=None, *, mode=True):
    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not mode:
                func_result = func(*args, **kwargs)
                return func_result
            start = time.perf_counter()
            func_result = func(*args, **kwargs)
            end = time.perf_counter()
            print(f'Function {func.__name__} takes: {end - start:.8f} secs')
            return func_result

        return wrapper

    if _func is None:
        return timer
    else:
        return timer(_func)
