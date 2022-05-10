from functools import total_ordering

# @total_ordering
class Money:
    def __init__(self, value, currency="USD"):
        self.exchange_rate = {"EUR": 0.93,
                              "BYN": 2.1,
                              "USD": 1}
        self.value = value
        self.currency = currency
        self.usd_value = self.value * self.exchange_rate[self.currency]


    def convert_to_def(self):

    def __add__(self, other):

            return str(round((self.usd_value + other.usd_value)/self.exchange_rate[self.currency], 2))+ ' ' + self.currency


    # __radd__ = __add__
    #
    # def __mul__(self, other):
    #     self.usd_value * other
    #     return self
    #
    # __rmul__ = __mul__
    #
    # def __sub__(self, other):
    #     try:
    #         return self.value - other.value
    #     except:
    #         return self.value - other
    # __rsub__ = __sub__
    #
    # def __truediv__(self, other):
    #     try:
    #         return self.value / other.value
    #     except:
    #         return self.value / other
    # __rtruediv__ = __truediv__


x = Money(10, "BYN")
y = Money(11)
z = Money(12.34, "EUR")

print(y*10)
# print(z + 3.11 * x + y * 0.8)
# print(f"result in 'USD':{sum([x, y, z])}")