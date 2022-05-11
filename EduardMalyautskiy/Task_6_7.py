from functools import total_ordering


@total_ordering
class Money:
    exchange_rate = {"EUR": 0.93,
                     "BYN": 2.1,
                     "USD": 1}

    def __init__(self, value, currency="USD"):
        self.value = value
        self.currency = currency

    def __str__(self):
        return str(self.value) + ' ' + self.currency

    def convert_to_def(self):
        return self.value * Money.exchange_rate[self.currency]

    def __add__(self, other):
        if isinstance(other, int):
            return Money(round(self.value + other / Money.exchange_rate[self.currency], 2), self.currency)

        return Money(round(self.value + other.convert_to_def() / Money.exchange_rate[self.currency], 2), self.currency)

    __radd__ = __add__

    def __mul__(self, other):
        return Money(self.value * other, self.currency)

    __rmul__ = __mul__

    def __sub__(self, other):
        return Money(round(self.value - other.convert_to_def() / Money.exchange_rate[self.currency], 2), self.currency)

    __rsub__ = __sub__

    def __truediv__(self, other):
        return Money(self.value / other, self.currency)

    __rtruediv__ = __truediv__

    def __lt__(self, other):
        return self.value < other.convert_to_def() / Money.exchange_rate[self.currency]

    def __eq__(self, other):
        return self.value == other.convert_to_def() / Money.exchange_rate[self.currency]

    def __le__(self, other):
        return self.value <= other.convert_to_def() / Money.exchange_rate[self.currency]
