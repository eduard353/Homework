from contextlib import ContextDecorator
import datetime
import random
import time


class IgnoreExceptLog(ContextDecorator):

    def __init__(self, filename = 'exec.log'):
        self.file = None
        self.filename =filename

    def __enter__(self):

        try:
            self.file = open(self.filename, 'a')

        except Exception as ex:
            print(f'Somthing was wrong {ex}')

        return self

    def __exit__(self, exception, type, tb):

        if exception is None:
            self.file.write(f'{datetime.datetime.now()}: There are no exception\n')
            print('There are no exception')
        if self.file is not None:

            self.file.close()
        return True


@IgnoreExceptLog()
def function():
    r = random.randint(2, 4)
    time.sleep(r)


@IgnoreExceptLog()
def function2():
    r = random.randint(2, 4)
    time.sleep(r)
    raise Exception('ERROR')

function()
