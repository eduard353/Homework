# Task 4.1

def reverse_quots(input_string):
    """
    function which receives a string and replaces all `"` symbols
    with `'` and vise versa.
    """

    split_input = input_string.split("'")
    output_list = []
    for i in split_input:
        output_list.append(i.replace('"', "'"))
    result = '"'.join(output_list)
    return result


reverse_quots('"sdsds"+ \' qweqwe \'python')
