from contextlib import ContextDecorator
import datetime
import random
import time


class mycontext(ContextDecorator):

    def __init__(self):
        self.file = None

    def __enter__(self):
        print('Starting')
        try:
            self.file = open('exec_time.log', 'a')
            self.file.write(f'Start time of execute: {datetime.datetime.now()} \n')
            raise ValueError('adada')

        except Exception as ex:
            print(f'Somthing was wrong {ex}')
    
        return self

    def __exit__(self, *exc):
        if self.file is not None:
            self.file.write(f'Stop time of execute: {datetime.datetime.now()} \n')
        print('Finishing')
        # return False


@mycontext()
def function():
    r = random.randint(2, 4)
    time.sleep(r)


function()
