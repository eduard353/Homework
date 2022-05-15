from contextlib import contextmanager


@contextmanager
def open_file(filename, mode='r'):

    file = None

    try:
        file = open(filename, mode=mode)
        yield file

    except FileNotFoundError as ex:
        print(f'File {filename} not found. ERROR: {ex}')

    except Exception as ex:
        print(f'Something was wrong. ERROR: {ex}')
    finally:

        if file is not None:
            file.close()


with open_file('1.txt') as f:
    print(f.read())
    f.apend()



