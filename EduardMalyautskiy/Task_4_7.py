# ### Task 4.7
# Implement a
# Example:
# ```python
# >>> foo([1, 2, 3, 4, 5])
# [120, 60, 40, 30, 24]
#
# >>> foo([3, 2, 1])
# [2, 3, 6]
# ```
#

def foo_func(input_list):
    """
    function `foo(List[int]) -> List[int]` which, given a list of
    integers, return a new list such that each element at index `i` of the new list
    is the product of all the numbers in the original array except the one at `i`.
    """

    result = []
    for x in range(0, len(input_list)):
        temp_list = input_list[:]
        temp_list.pop(x)
        temp_res = 1
        for y in temp_list:
            temp_res = temp_res * y
        result.append(temp_res)
    return result


print(foo_func([1, 1, 1]))
