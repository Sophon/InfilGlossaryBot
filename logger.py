import time


# Decorator function to track function calls
def count_calls(func):
    count = 0  # Initialize counter

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1  # Increment counter
        return func(*args, **kwargs)

    return wrapper


def log_call_count_of(function, rate):
    while True:
        print(function.__closure__[0].cell_contents)
        time.sleep(rate)

