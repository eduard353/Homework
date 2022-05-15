class OpenFile:

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode
        self.file = None



    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode)
            return self.file
        except FileNotFoundError:
            print(f'File {self.filename} not found')

    def __exit__(self, exception, value, trace):
        if self.file is not None:
            self.file.close()

        print('Exit')
        print(f"ERROR: {(exception)}")





with OpenFile('2.txt') as f:
    print(f.read())

