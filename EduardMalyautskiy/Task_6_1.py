### Task 4.1
'''
Implement a Counter class which optionally accepts the start value and the counter stop value.
If the start value is not specified the counter should begin with 0.
If the stop value is not specified it should be counting up infinitely.
If the counter reaches the stop value, print "Maximal value is reached."

Implement to methods: "increment" and "get"

* <em>If you are familiar with Exception rising use it to display the "Maximal value is reached." message.</em>

'''


class Counter:

    def __init__(self, start=0, stop=None):
        self.cur_value = start
        self.stop = stop

    def get(self):
        return self.cur_value

    def increment(self):
        if self.stop is not None:
            if self.cur_value == self.stop:
                try:
                    raise Exception('Maximal value is reached.')
                except Exception:
                    print('Maximal value is reached.')
                    return 'Maximal value is reached.'

        self.cur_value += 1
