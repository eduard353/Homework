from contextlib import ContextDecorator
import datetime
import random
import time


class ExecTimeLog(ContextDecorator):

    def __init__(self, filename='exec_time.log'):
        self.file = None
        self.filename = filename

    def __enter__(self):

        try:
            self.file = open(self.filename, 'a')
            self.file.write(f'Start time of execute: {datetime.datetime.now()}\n')


        except Exception as ex:
            print(f'Somthing was wrong {ex}')

        return self

    def __exit__(self, *exc):
        if self.file is not None:
            self.file.write(f'Stop time of execute: {datetime.datetime.now()}\n')
            self.file.close()

        return False


@ExecTimeLog()
def function():
    r = random.randint(2, 4)
    time.sleep(r)


function()
