import re


def most_common_words(filepath, number_of_words=3):
    with open(filepath, 'r') as f:
        word_dict = {}
        for line in f.readlines():
            opt_str = re.sub(r'[^\w\s]', '', line.lower())
            for word in opt_str.split():
                word_dict[word] = word_dict.get(word, 0) + 1

    word_list = []
    for k, v in word_dict.items():
        word_list.append((v, k))
    word_list.sort(reverse=True)
    print(word_list)
    return [word[1] for word in word_list[:number_of_words]]


print(most_common_words('../data/lorem_ipsum.txt'))
