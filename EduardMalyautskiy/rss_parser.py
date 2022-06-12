import argparse
import sys
from bs4 import BeautifulSoup
import requests
import logging

VERSION = '0.9.1'

headers = {
    'User-Agent': 'your-user-agent-here'
}

keys_dict = {
    "title": "Title",
    "link": "Link",
    "atom:link": "Link",
    "pubdate": "Date",
    "description": "Description",
    "source": "Source",
    "media:content": "Media",

}


def createParser():
    """
    Функция для парсинга параметров командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    return parser


class ReadRss:
    """
    Класс парсера RSS ленты
    """

    def __init__(self, rss_url, limit, headers):

        self.url = rss_url
        self.headers = headers
        self.limit = limit

    def get_rss(self):
        try:
            self.r = requests.get(self.url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', self.url)
            print(e)
            sys.exit()

    def parse(self):
        try:
            self.soup = BeautifulSoup(self.r.text, 'lxml')
            if 'xml' not in self.soup.contents[0]:
                # TODO реализовать собственное исключение и через него обработать невалидную ссылку
                print('There are not RSS feed link')
                sys.exit()
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)
        self.feed = self.soup.find('channel').find('title').text
        self.articles = self.soup.findAll('item')
        self.tags = set()
        # print(self.articles[0].contents)
        for tag in self.articles[0].contents:
            # print(tag)
            if tag == '\n' or tag.name is None:
                continue
            self.tags.add(tag.name)
        self.articles_dicts = []

        for a in self.articles[:self.limit]:
            # print(a)
            item_to_dict = dict()
            for tag in self.tags:
                try:
                    text = self.formatdata(str(a.find(tag).text))

                    if text is not None and text != '':
                        item_to_dict[tag] = text
                    elif 'href' in a.find(tag).attrs:
                        item_to_dict[tag] = text + '(' + a.find(tag)['href'] + ')'
                    elif 'url' in a.find(tag).attrs:
                        item_to_dict[tag] = text + '(' + a.find(tag)['url'] + ')'
                    elif tag == 'link':
                        item_to_dict[tag] = a.find(tag).next_sibling.replace('\n', '').replace('\t', '')

                except AttributeError as e:
                    print(f'Could not find tag "{tag}" in item.')
                    print(e)
            self.articles_dicts.append(item_to_dict)

    def print_data(self):

        #TODO посмотреть возможные проблемы кодировокку
        print('Feed: ', self.feed, end='\n\n')

        for item in self.articles_dicts:

            for tag in self.tags:
                if keys_dict.get(tag) and item.get(tag):
                    print(f'{keys_dict[tag]}: ', item.get(tag))

            print('-' * 60)

    @staticmethod
    def formatdata(data):
        result = data.replace('\n', '').replace('\t', '').replace('<![CDATA[', '').replace(']]>', '')
        return result


def run():
    parser = createParser()
    namespace = parser.parse_args()

    if namespace.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    feed = ReadRss(namespace.source.replace("'", ''), namespace.limit, headers)
    feed.get_rss()
    feed.parse()
    feed.print_data()



if __name__ == '__main__':
    run()

