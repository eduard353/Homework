class MyNumberCollection:

    def __init__(self, start, stop=None, step=None):
        self.data = []
        if '__iter__' in dir(start):
            for x in start:
                if isinstance(x, (int, float)):
                    self.data.append(x)
                else:
                    raise TypeError('MyNumberCollection supports only numbers!')
        else:
            if isinstance(start, (int, float)) and \
                    isinstance(stop, (int, float)) and \
                    isinstance(step, (int, float)):

                for x in range(start, stop, step):
                    self.data.append(x)
                if stop not in self.data:
                    self.data.append(stop)

    def append(self, num):
        if isinstance(num, (int, float)):
            self.data.append(num)
        else:

            raise TypeError(f'{num} - object is not a number!')

    def __add__(self, other):
        self.sum = self.data[:]
        if '__iter__' in dir(other):
            for x in other:
                if isinstance(x, (int, float)):
                    self.sum.append(x)
        return f'{self.sum}'

    def __getitem__(self, item):
        return self.data[item] ** 2

    def __iter__(self):
        self.item = 0
        return self

    def __next__(self):
        if self.item >= len(self.data):
            raise StopIteration
        else:
            self.item += 1
            return self.data[self.item - 1]

    def __str__(self):
        return f'{self.data}'


col1 = MyNumberCollection(0, 5, 2)
print(col1)
# [0, 2, 4, 5]
col2 = MyNumberCollection((1, 2, 3, 4, 5))
print(col2)
# [1, 2, 3, 4, 5]
# col3 = MyNumberCollection((1,2,3,"4",5))
# TypeError: MyNumberCollection supports only numbers!
col1.append(7)
print(col1)
# [0, 2, 4, 5, 7]
# col2.append("string")
# TypeError: 'string' - object is not a number!
print(col1 + col2)
# [0, 2, 4, 5, 7, 1, 2, 3, 4, 5]
print(col1)
# [0, 2, 4, 5, 7]
print(col2)
# [1, 2, 3, 4, 5]
print(col2[4])
# 25
for item in col1:
    print(item)
# >>> 0 2 4 5 7
