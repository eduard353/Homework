def call_once(func):
    cache = None

    def wrapper(*args):
        nonlocal cache
        if cache is None:
            cache = func(*args)
        return cache

    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


print(sum_of_numbers(13, 42))

print(sum_of_numbers(999, 100))

print(sum_of_numbers(134, 412))

print(sum_of_numbers(856, 232))
