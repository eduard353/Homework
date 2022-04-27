# ### Task 4.10


def generate_squares(num):
    """
    function that takes a number as an argument and returns a dictionary,
    where the key is a number and the value is the square of that number.
    """

    result = {x: x ** 2 for x in range(1, num + 1)}
    return result


print(generate_squares(5))
