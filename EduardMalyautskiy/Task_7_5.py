class MyCustomException(Exception):
    pass


class NoValue(MyCustomException):
    pass


class StringValue(MyCustomException):
    pass


class NotIntValue(MyCustomException):
    pass


def check_even(number=None):
    try:
        if number is None:
            raise NoValue('The required argument was not passed. One integer argument is expected.')

        elif isinstance(number, str):
            raise StringValue(f'One string argument is passed - {number}. One integer argument is expected.')

        elif not isinstance(number, int):
            raise NotIntValue(f'One not integer argument is passed - {number}. One integer argument is expected.')
        else:
            return number % 2 == 0
    except Exception as ex:
        print(f'{ex}')
        return False


check_even('dsdsd')
