import functools
import time

def func_timer(_func=None,*,mode=True):
    def timer(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            if mode == False:
                func_result = func(*args, **kwargs)
                return func_result
            start = time.perf_counter()
            func_result = func(*args,**kwargs)
            end = time.perf_counter()
            print(f'Function {func.__name__} takes: {end-start:.8f} secs')
            return func_result
        return wrapper




    if _func == None:
        return timer
    else:
        return timer(_func)