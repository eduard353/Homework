class EvenRange:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        if start % 2 == 0:
            self.cur = start
        else:
            self.cur = start + 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur >= self.end:
            print('Out of numbers!')
            raise StopIteration

        else:
            self.cur += 2
            return self.cur - 2
