class EvenRange:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        if start % 2 ==0:
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



er1 = EvenRange(7,11)
print(next(er1))
# 8
print(next(er1))
# 10
print(next(er1))
# "Out of numbers!"
print (next(er1))
# "Out of numbers!"
er2 = EvenRange(3, 14)
for number in er2:
    print(number)
# 4 6 8 10 12 "Out of numbers!"
