import time


def endless_fib_generator():
    prev1 = 0
    cur = 1

    while True:
        yield cur
        prev1, cur = cur, prev1 + cur


gen = endless_fib_generator()
while True:
    print(next(gen))
    time.sleep(2)
