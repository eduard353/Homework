class Chiper:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, key_word):
        self.key_word = key_word
        self.encode_alphabet = key_word.upper()
        for x in Chiper.alphabet:
            if x not in self.encode_alphabet[:]:
                self.encode_alphabet += x
        print(Chiper.alphabet)
        print(self.encode_alphabet)

    def encode(self, text):
        self.encode_word = ''
        for x in text:
            if x.isalpha():
                symb = self.encode_alphabet[Chiper.alphabet.index(x.upper())]
                if x.islower():
                    symb = symb.lower()
                self.encode_word += symb
            else:
                self.encode_word += x
        return self.encode_word

    def decode(self, text):
        self.decode_word = ''
        for x in text:
            if x.isalpha():
                symb = Chiper.alphabet[self.encode_alphabet.index(x.upper())]
                if x.islower():
                    symb = symb.lower()
                self.decode_word += symb
            else:
                self.decode_word += x
        return self.decode_word
