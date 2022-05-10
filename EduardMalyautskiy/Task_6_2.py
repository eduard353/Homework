class HistoryDict:

    def __init__(self, hist_dict={}):
        self.hist_dict = hist_dict
        self.history = []

    def set_value(self, key, value):
        self.hist_dict[key] = value
        if len(self.history) == 10:
            self.history.pop(0)

        self.history.append(key)

    def get_history(self):
        return self.history
