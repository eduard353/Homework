# ### Task 4.9
# Implement a bunch of functions which receive a changeable number of strings and return next parameters:

import string


def test_1_1(*str_list):
    """
     characters that appear in all strings
    """
    result = set(str_list[0])
    for x in range(1, len(str_list)):
        result.intersection_update(set(str_list[x]))
    return result


print(test_1_1(*["hello", "world", "python", ]))


def test_1_2(*str_list):
    """
     characters that appear in at least one string
    """
    result = set(str_list[0])
    for x in range(1, len(str_list)):
        result.update(set(str_list[x]))
    return result


print(test_1_2(*["hello", "world", "python", ]))


def test_1_3(*str_list):
    """
     characters that appear at least in two strings
    """
    result = set()
    out = [[str_list[i], str_list[j]] for i in range(0, len(str_list)) for j in range(0, len(str_list)) if i < j]
    print(out)
    for x in out:
        result.update(set(x[0]) & set(x[1]))

    return result


print(test_1_3(*["hello", "world", "python", ]))


def test_1_4(*str_list):
    """
     characters of alphabet, that were not used in any string
    """
    result = set(string.ascii_lowercase)

    for x in str_list:
        result.difference_update(set(x))
    return result


print(test_1_4(*["hello", "world", "python", ]))
