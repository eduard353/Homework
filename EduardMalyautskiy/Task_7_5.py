class MyCustomException(Exception):

    def __init__(self, text):
        self.text = text


class NoValue(MyCustomException):
    pass


class StringValue(MyCustomException):
    pass


class NotIntValue(MyCustomException):
    pass


def check_even(number=None):
    if number is None:
        raise NoValue('The required argument was not passed. One integer argument is expected.')

    elif isinstance(number, str):
        raise StringValue(f'One string argument is passed - {number}. One integer argument is expected.')

    elif not isinstance(number, int):
        raise NotIntValue(f'One not integer argument is passed - {number}. One integer argument is expected.')
    else:
        return number % 2 == 0


print(check_even(12))
check_even(['Not INT', ])
