import argparse
import sys
from bs4 import BeautifulSoup
import requests
import logging
import parser_exceptions
import json
from dateutil.parser import parse

VERSION = '0.9.1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
}

keys_dict = {
    "title": "Title",
    "link": "Link",
    "atom:link": "Link",
    "pubdate": "Date",
    "description": "Description",
    "source": "Source",
    "media:content": "Media",
    "guid": "ID"

}


def parse_cli_args():
    """
    Функция для парсинга параметров командной строки
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', exit_on_error=False)
    parser.add_argument('source', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    return parser.parse_args()


def print_and_exit(msg):
    """Функция вывода сообщения и прекращения выполнения программы"""
    print(msg)
    sys.exit()


class ReadRss:
    """
    Класс парсера RSS ленты
    """

    def __init__(self, rss_url, limit, headers):

        self.url = rss_url
        self.headers = headers
        self.limit = limit
        self.tags = set()
        self.feed = ''
        self.articles_dicts = []

    def get_rss(self):
        """Функция получения данных из RSS ленты"""
        try:
            self.r = requests.get(self.url, headers=self.headers)

            if self.r.status_code != 200:
                raise parser_exceptions.RequestProblem

        except parser_exceptions.RequestProblem:
            print_and_exit(f'Error receiving data from the server: {self.url}\n'
                           f'Response code received: {self.r.status_code}\n'
                           f'Check the correctness of the URL address')

        except requests.exceptions.HTTPError as http_err:
            print_and_exit(f'HTTP error occurred: {http_err}')

        except Exception as e:
            print_and_exit(f'Error fetching the data from URL: {self.url}\n'
                           f'Check the correctness of the URL address')

        try:
            self.soup = BeautifulSoup(self.r.text, 'lxml')
            if 'xml' not in self.soup.contents[0]:
                raise parser_exceptions.NoXMLException

        except parser_exceptions.NoXMLException as e:
            print_and_exit('There are not RSS feed link\n'
                           'Check the correctness of the URL address')


        except Exception as e:
            print_and_exit(f'Could not parse the xml: {self.url}')

        # self.encoding = self.soup.contents[0].replace('xml version="1.0" encoding="', '').replace('"?', '')

        try:
            self.feed = self.soup.find('channel').find('title').text
            self.articles = self.soup.findAll('item')
            if self.articles is None:
                raise parser_exceptions.NoItemsException
        except parser_exceptions.NoItemsException as e:
            print_and_exit('There are no items in RSS')

        except AttributeError as e:
            print_and_exit('Incorrect RSS structure, missing channel title tag')

        for tag in self.articles[0].contents:
            # print(tag)
            if tag == '\n' or tag.name is None:
                continue
            self.tags.add(tag.name)

        for a in self.articles[:self.limit]:
            # print(a)
            item_to_dict = dict()
            for tag in self.tags:
                try:
                    text = self.formatdata(str(a.find(tag).text))
                    if text is not None and text != '':
                        if tag == 'pubdate':
                            print(parse(text).date())
                            item_to_dict[tag] = parse(text).date().strftime('%Y.%m.%d')
                        else:
                            item_to_dict[tag] = text
                        # item_to_dict[tag] = text
                    elif 'href' in a.find(tag).attrs:
                        item_to_dict[tag] = text + '(' + a.find(tag)['href'] + ')'
                    elif 'url' in a.find(tag).attrs:
                        item_to_dict[tag] = text + '(' + a.find(tag)['url'] + ')'
                    elif tag == 'link':
                        item_to_dict[tag] = a.find(tag).next_sibling.replace('\n', '').replace('\t', '')

                except AttributeError as e:
                    print(f'Could not find tag "{tag}" in item. Skip it.')

            self.articles_dicts.append(item_to_dict)

    def print_data(self):
        """Функция печати данных в командную строку"""
        # TODO посмотреть возможные проблемы кодировокку

        print('Feed: ', self.feed, end='\n\n')

        for item in self.articles_dicts:

            for tag in self.tags:
                if keys_dict.get(tag) and item.get(tag):
                    print(f'{keys_dict[tag]}: ', item.get(tag))

            print('-' * 60)

    def print_json(self):
        """Функция печати данных в командную строку в формате JSON"""
        print(json.dumps(self.articles_dicts, ensure_ascii=False))

    @staticmethod
    def formatdata(data):
        result = data.replace('\n', '').replace('\t', '').replace('<![CDATA[', '').replace(']]>', '')
        return result




def run():
    """Основная функция запускающая программу"""
    try:
        namespace = parse_cli_args()
    except Exception as e:
        print('You have specified an invalid command line argument value.')
        print(e)
        sys.exit()

    if namespace.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    feed = ReadRss(namespace.source.replace("'", ''), namespace.limit, headers)

    feed.get_rss()

    if namespace.json:
        feed.print_json()
    else:
        feed.print_data()


if __name__ == '__main__':
    run()
