def remember_result(func):
    last_result = None
    def save_last_result(*args):

        nonlocal last_result
        print(f"Last result = '{last_result}'")
        last_result = func(*args)
    return save_last_result



@remember_result
def sum_list(*args):
    result = ""

    # if all(isinstance(i, int) for i in args):
    #     result = 0
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result

sum_list("a", "b")
sum_list("abc", "cde")
sum_list(3, 4, 5)

