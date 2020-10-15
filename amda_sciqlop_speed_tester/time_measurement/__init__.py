import time


def exec_time(function,*args,**kwargs):
    start = time.perf_counter_ns()
    result = function(*args,**kwargs)
    stop = time.perf_counter_ns()
    return result, start, stop

