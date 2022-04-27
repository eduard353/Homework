# Task 4.2
import re


def check_polindrome(input_string):
    """
    function that check whether a string is a palindrome or not. Usage of
    any reversing functions is prohibited
    """

    input_string = ''.join(input_string.lower().split(' '))
    opt_str = re.sub(r'[^\w\s]', '', input_string)
    rev_str = opt_str[-1::-1]
    if opt_str == rev_str:
        return True
    else:
        return False


print(check_polindrome('Mr. Owl ate my metal worm'))
