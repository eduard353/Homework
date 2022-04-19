# # Python Practice - Session 2
#
# ### Task 2.1
# Write a Python program to calculate the length of a string without using the `len` function.
#


def calc_len(input_string='Test string'):
    """
    Сalculate the length of a string without using the `len` function.
    """
    str_len = 0
    for _ in input_string:
        str_len += 1
    print(f'Длина строки "{input_string}": ', str_len)

    return str_len


# ### Task 2.2
# Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).
# Examples:
# ```
# Input: 'Oh, it is python'
# Output: {',': 1, ' ': 3, 'o': 2, 'h': 2, 'i': 2, 't': 2, 's': 1, 'p': 1, 'y': 1, 'n': 1}
# ```


def calc_cnt_char(input_string='Test string'):
    """
     Count the number of characters (character frequency) in a string (ignore case of letters).
    """

    out_dict = dict()
    for symbol in input_string:
        if out_dict.get(symbol) is None:
            out_dict[symbol] = 1
        else:
            out_dict[symbol] += 1
    print(out_dict)

    return out_dict


#
# ### Task 2.3
# Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.
# Examples:
# ```
# Input: ['red', 'white', 'black', 'red', 'green', 'black']
# Output: ['black', 'green', 'red', 'white', 'red']
# ```


def get_unq_words(input_list=['red', 'white', 'black', 'red', 'green', 'black']):
    """
     program that accepts a comma separated sequence of words as input and prints the unique words in sorted form.
    """
    output_list = sorted(list(set(input_list)))
    print(output_list)

    return output_list


#
# ### Task 2.3
# Create a program that asks the user for a number and then prints out a list of all the [divisors](https://en.wikipedia.org/wiki/Divisor) of that number.
# Examples:
# ```
# Input: 60
# Output: {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60}
# ```


def get_list_of_divisors(input_number=60):
    """
     program that asks the user for a number and then prints out a list of all the [divisors]
    """
    all_divisors = set()
    for _ in range(1, input_number + 1):
        if input_number % _ == 0:
            all_divisors.add(_)
    print("Все делители числа - ", input_number, ': ', set(sorted(all_divisors)))

    return set(sorted(all_divisors))


#
# ### Task 2.4
# Write a Python program to sort a dictionary by key.


def sort_dict(input_dict={'a': 1, 'b': 3, 'e': 4, 'c': 5}):
    """
     program to sort a dictionary by key
    """
    dict_keys = list(input_dict.keys())
    dict_keys.sort()
    sorted_dict = dict()
    for key in dict_keys:
        sorted_dict[key] = input_dict[key]

    print('Отсортированный словарь:', sorted_dict)

    return sorted_dict


#
# ### Task 2.5
# Write a Python program to print all unique values of all dictionaries in a list.
# Examples:
# ```
# Input: [{"V":"S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII":"S005"}, {"V":"S009"},{"VIII":"S007"}]
# Output: {'S005', 'S002', 'S007', 'S001', 'S009'}
# ```


def get_unq_values(input_list_of_dict=[{"V": "S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII": "S005"},
                                       {"V": "S009"}, {"VIII": "S007"}]):
    """
     program to print all unique values of all dictionaries in a list
    """
    output_set = set()
    for _ in input_list_of_dict:
        output_set.update(_.values())
    print(output_set)

    return output_set


#
# ### Task 2.6
# Write a Python program to convert a given tuple of positive integers into an integer.
# Examples:
# ```
# Input: (1, 2, 3, 4)
# Output: 1234
# ```


def convert_tuple_to_integer(input_tuple=(1, 2, 3, 4)):
    """
    program to convert a given tuple of positive integers into an integer.
    """

    output = ''
    for digit in input_tuple:
        output += str(digit)
    output = int(output)
    print(output)

    return output


#
#
# ### Task 2.7
# Write a program which makes a pretty print of a part of the multiplication table.
# Examples:
# ```
# Input:
# a = 2
# b = 4
# c = 3
# d = 7
#
# Output:
# 	3	4	5	6	7
# 2	6	8	10	12	14
# 3	9	12	15	18	21
# 4	12	16	20	24	28
# ```
#


def print_multipl_table(list_of_multi=[2, 4, 3, 7]):
    """
     program which makes a pretty print of a part of the multiplication table.
    """
    list_of_multi.sort()
    while True:
        print('', end='\t')
        for x in range(1, 10):
            print(x, end='\t')
        print()
        for d in list_of_multi:
            print(d, end='\t')
            for x in range(1, 10):
                print(d * x, end='\t')
            print()
        break


# ### Materials
# * [Python Data Types](https://realpython.com/python-data-types/)
# * [Python Data Structures](https://realpython.com/python-data-structures/)
# * [Conditional Statements](https://realpython.com/python-conditional-statements/)
# * [While loop](https://realpython.com/python-while-loop/)
# * [For loop](https://realpython.com/python-for-loop/)
# * [Operators](http://pythonicway.com/python-operators)


calc_len()
calc_cnt_char()
get_unq_words()
get_list_of_divisors()
sort_dict()
get_unq_values()
convert_tuple_to_integer()
print_multipl_table()
