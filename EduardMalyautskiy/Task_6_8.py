class Pagination:

    def __init__(self, text, per_page):
        self.text = text
        self.per_page = per_page
        self.item_count = len(text)
        self.page_count = self.item_count // self.per_page + 1
        self.pg_info = {key: int(val) for key, val in enumerate(str(per_page) * (self.page_count - 1))}
        self.pg_info[self.item_count // self.per_page] = self.item_count % self.per_page
        self.pages = {key: value for key, value
                      in enumerate(text[i:i + per_page] for i in range(0, len(text), per_page))}
        print(self.pages)

    def count_items_on_page(self, pg_num):
        try:
            return len(self.pages[pg_num])
        except KeyError:
            print("Invalid index. Page is missing")

    def display_page(self, page_num):

        return self.pages[page_num]

    def find_page(self, string):
        result = []
        beg = 0
        while True:

            index = self.text.find(string, beg)
            if result == [] and index == -1:
                raise Exception(f'{string} is missing on the pages')
                break
            elif result != [] and index == -1:

                return result
            elif index != -1:

                if index // self.per_page == (index + len(string)) // self.per_page:
                    result.append(index // self.per_page)
                else:
                    for x in range(index // self.per_page, (index + len(string)) // self.per_page + 1):
                        result.append(x)
            beg = beg + index + 1
