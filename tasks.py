# Simulated dummy tasks

import time

def add(params, task_state):
    a = params.get("a", 0)
    b = params.get("b", 0)
    for i in range(15):
        time.sleep(1)
        with task_state.lock:
            if task_state.cancelled:
                return None
            while task_state.paused:
                task_state.lock.wait()
    return a + b

def fib(params, task_state):
    n = params.get("n", 10)
    def fib_inner(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    for i in range(15):
        time.sleep(1)
        with task_state.lock:
            if task_state.cancelled:
                return None
            while task_state.paused:
                task_state.lock.wait()
    return fib_inner(n)
