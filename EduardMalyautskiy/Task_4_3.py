# Task 4.3


def str_split(input_string, sep):
    """
     function which works the same as `str.split` method
    """
    result = []

    while True:
        end_pos = input_string[:].find(sep)
        if end_pos == -1:
            result.append(input_string[:])
            break
        else:
            result.append(input_string[:end_pos])
        input_string = input_string[end_pos + len(sep):]

    return result


print(str_split('123aa4562a789', 'zz'))
print(str_split('123aa4562a789', 'a'))
