# ### Task 4.6


def get_longest_word(input_string):
    """
    function `get_shortest_word(s: str) -> str` which returns the
    longest word in the given string. The word can contain any symbols except
    whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
    the string with a same length return the word that occures first.
    """

    symb_for_replace = ["\n", "\t", "\f", "\a", "\v", "\r", "\b"]
    for s in symb_for_replace:
        input_string = input_string.replace(s, ' ')

    split_string = input_string.split()
    result = split_string[0]
    for x in split_string[1:]:
        if len(x) > len(result): result = x
    return result


print(get_longest_word("sdfsdf sdfsf\nsdssssssssssfs\tsdaaaafsdf"))
