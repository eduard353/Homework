# ### Task 4.5

def get_digits(num):
    """
    function `get_digits(num: int) -> Tuple[int]` which returns a tuple
    of a given integer's digits.
    """

    result = tuple(int(x) for x in str(num))

    return result


print(get_digits(112233))
