import time


# Decorator function to track function calls
def count_calls(func):
    count = 0  # Initialize counter

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1  # Increment counter
        return func(*args, **kwargs)

    return wrapper


def write_to_file(output, filename):
    with open(filename, 'a') as file:
        file.write(output + "\n")
        file.close()


def log_call_count_of(function, rate, log_to_file=False, filename=""):
    output = str(function.__closure__[0].cell_contents)
    while True:
        if log_to_file is True:
            write_to_file(output, filename)
        else:
            print("function called " + output + " times")

        time.sleep(rate)

