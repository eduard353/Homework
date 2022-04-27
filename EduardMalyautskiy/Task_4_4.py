# ### Task 4.4


def split_by_index(input_string, indexes):
    """
    function `split_by_index(s: str, indexes: List[int]) -> List[str]`
    which splits the `s` string by indexes specified in `indexes`. Wrong indexes
    must be ignored.
    """

    indexes = sorted(list(set(filter(lambda x: isinstance(x, int) and x < len(input_string), indexes))))

    if indexes == []:
        return [input_string]
    indexes.insert(0, 0)
    slices = []

    for i in range(0, len(indexes) - 1):
        slices.append([indexes[i], indexes[i + 1]])

    if indexes[-1] < len(input_string):
        slices.append([indexes[-1], len(input_string)])
    result = []

    for s in slices:
        result.append(input_string[s[0]:s[1]])

    return result


print(split_by_index("pythoniscool,isn'tit?", [500]))
print(split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]))
print(["python", "is", "cool", ",", "isn't", "it?"])
