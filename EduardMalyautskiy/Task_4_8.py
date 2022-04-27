# ### Task 4.8
# Implement a
# Example:
# ```python
# >>> get_pairs([1, 2, 3, 8, 9])
# [(1, 2), (2, 3), (3, 8), (8, 9)]
#
# >>> get_pairs(['need', 'to', 'sleep', 'more'])
# [('need', 'to'), ('to', 'sleep'), ('sleep', 'more')]
#
# >>> get_pairs([1])
# None
# ```
#

def get_pairs(input_list):
    """
    function `get_pairs(lst: List) -> List[Tuple]` which returns a list
    of tuples containing pairs of elements. Pairs should be formed as in the
    example. If there is only one element in the list return `None` instead.
    """

    if len(input_list) < 2:
        return

    else:

        result = [(input_list[i], input_list[i + 1]) for i in range(0, len(input_list) - 1)]

        return result


print(get_pairs(['need', 'to', 'sleep', 'more']))
