import argparse
import sys
from bs4 import BeautifulSoup
import requests
import logging
import parser_exceptions
import json
from dateutil.parser import parse

VERSION = '0.9.1'

HEADERS = {
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


def parse_cli_args(commands=None):
    """
    Функция для парсинга параметров командной строки
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', exit_on_error=False)
    parser.add_argument('source', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    return parser.parse_args(commands)


def print_and_exit(msg):
    """Функция вывода сообщения и прекращения выполнения программы"""
    print(msg)
    sys.exit()


class ReadRss:
    """
    Класс парсера RSS ленты
    """

    def __init__(self, rss_url, limit):

        self.url = rss_url
        self.feed, self.articles = ReadRss.parse_rss(ReadRss.get_rss(rss_url))
        self.limit = limit
        self.tags = ReadRss.get_tags(self.articles)

        self.articles_dicts = ReadRss.items_to_dict(self.articles, self.tags, self.limit)


    @staticmethod
    def get_rss(url):
        """Функция получения данных из RSS ленты"""
        try:
            response= requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
        })

            if response.status_code != 200:
                raise parser_exceptions.RequestProblem

        except parser_exceptions.RequestProblem:
            print_and_exit(f'Error receiving data from the server: {url}\n'
                           f'Response code received: {response.status_code}\n'
                           f'Check the correctness of the URL address')

        except requests.exceptions.HTTPError as http_err:
            print_and_exit(f'HTTP error occurred: {http_err}')

        except Exception as e:
            print_and_exit(f'Error fetching the data from URL: {url}\n'
                           f'Check the correctness of the URL address')

        return response

    @staticmethod
    def parse_rss(response):

        try:
            soup = BeautifulSoup(response.text, 'xml')

            if not soup.find('rss'):
                raise parser_exceptions.NotRSSException

        except parser_exceptions.NotRSSException as e:
            print_and_exit('There are not RSS feed link\n'
                           'Check the correctness of the URL address')


        except Exception as e:
            print_and_exit('Could not parse the rss')
            print(e)

        # self.encoding = self.soup.contents[0].replace('xml version="1.0" encoding="', '').replace('"?', '')

        try:
            feed = soup.find('channel').find('title').text
            articles = soup.findAll('item')
            if articles is None:
                raise parser_exceptions.NoItemsException
        except parser_exceptions.NoItemsException as e:
            print_and_exit('There are no items in RSS')

        except AttributeError as e:
            print_and_exit('Incorrect RSS structure, missing channel title tag')
        print(articles)
        return (feed, articles)

    @staticmethod
    def get_tags(articles):
        tags = set()
        for tag in articles[0].contents:
            # print(tag)
            if tag == '\n' or tag.name is None:
                continue
            tags.add(tag.name)
        return tags

    @staticmethod
    def items_to_dict(articles, tags, limit=None):
        articles_dicts = []
        for a in articles[:limit]:
            # print(a)
            item_to_dict = dict()
            for tag in tags:
                try:
                    text = ReadRss.formatdata(str(a.find(tag).text))
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

            articles_dicts.append(item_to_dict)
        return articles_dicts

    def print_data(self):
        """Функция печати данных в командную строку"""
        # TODO посмотреть возможные проблемы кодировокку

        print('Feed: ', self.feed, end='\n\n')

        for item in self.articles_dicts:

            for key in keys_dict.keys():
                if item.get(key):
                    print(f'{keys_dict[key]}: ', item.get(key))

            print('-' * 60)

    def print_json(self):
        """Функция печати данных в командную строку в формате JSON"""
        print(json.dumps(self.articles_dicts, ensure_ascii=False))

    @staticmethod
    def formatdata(data):
        result = data.replace('\n', '').replace('\t', '').replace('<![CDATA[', '').replace(']]>', '').strip()
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

    feed = ReadRss(namespace.source.replace("'", ''), namespace.limit)

    if namespace.json:
        feed.print_json()
    else:
        feed.print_data()


if __name__ == '__main__':
    run()
