from contextlib import ContextDecorator
import time


class mycontext(ContextDecorator):

    def __enter__(self):
        print('Starting')
        return self

    def __exit__(self, *exc):
        print('Finishing')
        return False


@mycontext()
def function():
    pass


function()
