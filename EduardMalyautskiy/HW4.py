import re

# # Python Practice - Session 4
#
#
# ### Task 4.1
# Implement a function which receives a string and replaces all `"` symbols
# with `'` and vise versa.


def reverse_quots(input_string):
    split_input = input_string.split("'")
    output_list = []
    for i in split_input:
        output_list.append(i.replace('"', "'"))
    result = '"'.join(output_list)
    print(result)
    return result


reverse_quots('"sdsds"+ \' qweqwe \'python')

#
# ### Task 4.2
# Write a function that check whether a string is a palindrome or not. Usage of
# any reversing functions is prohibited. To check your implementation you can use
# strings from [here](https://en.wikipedia.org/wiki/Palindrome#Famous_palindromes).
#


def check_polindrome(input_string):
    input_string =''.join(input_string.lower().split(' '))
    opt_str = re.sub(r'[^\w\s]', '', input_string)
    rev_str = opt_str[-1::-1]
    if opt_str == rev_str:
        return True
    else:
        return False


print(check_polindrome('Mr. Owl ate my metal worm'))
# ### Task 4.3
# Implement a function which works the same as `str.split` method
# (without using `str.split` itself, ofcourse).
#


def str_split(input_string, sep):

    result = []

    while True:
        end_pos = input_string[:].find(sep)
        if end_pos == -1:
            result.append(input_string[:])
            break
        else:
            result.append(input_string[:end_pos])
        input_string = input_string[end_pos+len(sep):]

    return result

print(str_split('123aa4562a789', 'zz'))
print('123aa4562a789'.split('zz'))

# ### Task 4.4
# Implement a function `split_by_index(s: str, indexes: List[int]) -> List[str]`
# which splits the `s` string by indexes specified in `indexes`. Wrong indexes
# must be ignored.
# Examples:
# ```python
# >>> split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])
# ["python", "is", "cool", ",", "isn't", "it?"]
#
# >>> split_by_index("no luck", [42])
# ["no luck"]
# ```
#

def split_by_index(input_string, indexes):

    for i in indexes[:]:

        if not isinstance(i, int) or i >= len(input_string):

            indexes.remove(i)



    indexes = sorted(list(set(indexes)))
    if indexes == []:
        return [input_string]
    indexes.insert(0, 0)
    slices = []

    for i in range(0, len(indexes)-1):
        slices.append([indexes[i], indexes[i+1]])

    if indexes[-1] < len(input_string):
        slices.append([indexes[-1], len(input_string)])
    print(slices)

    result = []

    for s in slices:
        result.append(input_string[s[0]:s[1]])


    return result

print(split_by_index("pythoniscool,isn'tit?", [500]))
print(split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]))
print(["python", "is", "cool", ",", "isn't", "it?"])
# split_by_index('aaaaaaaaa', [1,7 ,3 , 3, 5, 6, 4, 3.0, 3.5, 3.5, 'a'])


# ### Task 4.5
# Implement a function `get_digits(num: int) -> Tuple[int]` which returns a tuple
# of a given integer's digits.
# Example:
# ```python
# >>> split_by_index(87178291199)
# (8, 7, 1, 7, 8, 2, 9, 1, 1, 9, 9)
# ```
#


def get_digits(num):

    str_num = str(num)
    result = []
    for x in str_num:
        result.append(int(x))
    return tuple(result)

print(get_digits(112233))

# ### Task 4.6
# Implement a function `get_shortest_word(s: str) -> str` which returns the
# longest word in the given string. The word can contain any symbols except
# whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
# the string with a same length return the word that occures first.
# Example:
# ```python
#
# >>> get_shortest_word('Python is simple and effective!')
# 'effective!'
#
# >>> get_shortest_word('Any pythonista like namespaces a lot.')
# 'pythonista'
# ```
#

def get_longest_word(input_string):
    symb_for_replace = ["\n", "\t", "\f", "\a", "\v", "\r", "\b"]
    for s in symb_for_replace:
        input_string = input_string.replace(s, ' ')
    print(input_string)
    split_string = input_string.split()
    result = split_string[0]
    for x in split_string[1:]:
        if len(x) > len(result): result = x
    return result

print(get_longest_word("sdfsdf sdfsf\nsdssssssssssfs\tsdaaaafsdf"))
# ### Task 4.7
# Implement a function `foo(List[int]) -> List[int]` which, given a list of
# integers, return a new list such that each element at index `i` of the new list
# is the product of all the numbers in the original array except the one at `i`.
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

# ### Task 4.8
# Implement a function `get_pairs(lst: List) -> List[Tuple]` which returns a list
# of tuples containing pairs of elements. Pairs should be formed as in the
# example. If there is only one element in the list return `None` instead.
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

    if len(input_list) < 2: return

    else:
        result = []

        for i in range(0, len(input_list) - 1):
            result.append((input_list[i], input_list[i + 1]))

        return result

print(get_pairs(['need', 'to', 'sleep', 'more']))
# ### Task 4.9
# Implement a bunch of functions which receive a changeable number of strings and return next parameters:
#
# 1) characters that appear in all strings
#
# 2) characters that appear in at least one string
#
# 3) characters that appear at least in two strings
#
# 4) characters of alphabet, that were not used in any string
#
# Note: use `string.ascii_lowercase` for list of alphabet letters
#
# ```python
# test_strings = ["hello", "world", "python", ]
# print(test_1_1(*strings))
# >>> {'o'}
# print(test_1_2(*strings))
# >>> {'d', 'e', 'h', 'l', 'n', 'o', 'p', 'r', 't', 'w', 'y'}
# print(test_1_3(*strings))
# >>> {'h', 'l', 'o'}
# print(test_1_4(*strings))
# >>> {'a', 'b', 'c', 'f', 'g', 'i', 'j', 'k', 'm', 'q', 's', 'u', 'v', 'x', 'z'}
# ```
#

def test_1_1(str_list):
    result = set(str_list[0])
    for x in range(1, len(str_list)):
        result.intersection_update(set(str_list[x]))
    return result

print(test_1_1(["hello", "world", "python", ]))

def test_1_2(str_list):
    result = set(str_list[0])
    for x in range(1, len(str_list)):
        result.update(set(str_list[x]))
    return result

print(test_1_2(["hello", "world", "python", ]))




# ### Task 4.10
# Implement a function that takes a number as an argument and returns a dictionary, where the key is a number and the value is the square of that number.
# ```python
# print(generate_squares(5))
# >>> {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
# ```
#
# ### Task 4.11
# Implement a function, that receives changeable number of dictionaries (keys - letters, values - numbers) and combines them into one dictionary.
# Dict values ​​should be summarized in case of identical keys
#
# ```python
# def combine_dicts(*args):
#     ...
#
# dict_1 = {'a': 100, 'b': 200}
# dict_2 = {'a': 200, 'c': 300}
# dict_3 = {'a': 300, 'd': 100}
#
# print(combine_dicts(dict_1, dict_2)
# >>> {'a': 300, 'b': 200, 'c': 300}
#
#
# print(combine_dicts(dict_1, dict_2, dict_3)
# >>> {'a': 600, 'b': 200, 'c': 300, 'd': 100}
# ```
#
# ### Materials
# * [Scope](https://python-scripts.com/scope)
# * [Functions](https://python-scripts.com/functions-python)
# * [Defining your own python function](https://realpython.com/defining-your-own-python-function/)
# * [Python Lambda](https://realpython.com/python-lambda/)
#
