import argparse
import sys
from bs4 import BeautifulSoup
import requests
import logging
from parser_exceptions import IncorrectPath, NotRSSException, NoItemsException, RequestProblem
import json
from dateutil.parser import parse
from parser_db import DataConn
from converters import convert_to_html, save_to_html, save_to_pdf, get_file_local_path
from os import path
from progress.bar import Bar
from colorama import Fore, init
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


init(convert=True)

VERSION = '0.9.5'

# Dict of rss tags an their user-friendly names
keys_dict = {
    "title": "Title",
    "link": "Link",
    "atom:link": "Link",
    "pubdate": "Date",
    "description": "Description",
    "media:content": "Media",
    "content": "Media",
    "enclosure": "Media",
    "image": 'Media',


}

# Tags for save to DB
article_tags = ["Feed", "Title", "Date", "Link", "Description", "Source", "Media", "GUID"]


def parse_cli_args(commands=None):
    """
    Function for parsing command line parameters

    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', nargs='?', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--colorize', action='store_true',
                        help='That will print the result of the utility in colorized mode')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', help='It should take a date in YearMonthDay format. For example: --date 20191020. '
                                       'The cashed news can be read with it. The new from the specified day will '
                                       'be printed out. If the news are not found return an error.')
    parser.add_argument('--to_html', nargs='?', default=None, metavar='PATH',
                        help='Upload result to html-file in folder in PATH parameter,'
                             ' file name is current date with ms.')
    parser.add_argument('--to_pdf', nargs='?', default=None, metavar='PATH',
                        help='Upload result to pdf-file in folder in PATH parameter,'
                             ' file name is current date with ms.')
    parser.add_argument('--clear_cache', action='store_true', help='Delete data from cache DB.')

    return parser.parse_args(commands)


def print_and_exit(msg):
    """Function of message output and termination of program execution"""
    print(msg)
    sys.exit()


def clear_db(db=path.join(path.abspath(path.dirname(__file__)), 'rss_cache.db')):
    """
    Method delete cached data from DB
    :param db: DB path
    """
    with DataConn(db) as conn:
        logging.debug(f'Start clearing DB. DB path: {db}')
        conn.execute("DELETE FROM news")
        conn.commit()
        logging.debug(f'Clearing DB finished. DB path: {db}')


def remove_quots(text):
    """Function that removes quotation marks from the text"""
    if text:
        text = text.replace("'", '').replace('"', '')
    return text


def get_text_from_html(html):
    """Function that returns only text from an HTML file (fragment)"""
    soup = BeautifulSoup(html, features="html.parser")
    if soup.find('img'):
        media_link = soup.find('img').get('src')
    else:
        media_link = None
    return (soup.get_text(), media_link)



class ReadRss:
    """
    RSS Feed Parser class
    """

    def __init__(self, rss_url, limit, date=None):

        self.url = rss_url
        self.limit = limit
        if date:

            self.articles_dicts = self.get_news_from_db(date, self.url, self.limit)
        else:

            self.feed, self.articles = ReadRss.parse_rss(ReadRss.get_rss(rss_url))
            self.tags = ReadRss.get_tags(self.articles)
            self.articles_dicts = ReadRss.items_to_dict(self.articles, self.tags, self.limit, self.feed)

    @staticmethod
    def get_news_from_db(date, url=None, limit=None,
                         db=path.join(path.abspath(path.dirname(__file__)), 'rss_cache.db')):
        """
        Method of getting data from the database
        :param date: Date of articles
        :param url: Link to RSS feed
        :param limit: Number of articles received
        :param db: The path to the database of the storing article
        :return: list of articles in dict format
        """
        articles_dicts = []
        # Form an SQL query to the database based on the received parameters
        request_string = f"select * from news where Date='{date}'"
        if url:
            request_string += f" and Url='{url}'"
        if limit:
            request_string += ' limit ' + str(limit)

        with DataConn(db) as conn:
            logging.debug(f'News get from cache DB - {db}')
            logging.debug(f'Execute request: {request_string}')
            result = conn.execute(request_string).fetchall()
            if len(result) == 0:
                print_and_exit('No data in cache DB')

            for item in result:
                article = dict()

                article["Feed"] = item[1]
                article["Title"] = item[2]
                article["Link"] = item[3]
                article["Date"] = item[4]
                article["Description"] = item[5]
                article["Media"] = item[6]
                article['LocalImgLink'] = item[8]
                articles_dicts.append(article)

        return articles_dicts

    @staticmethod
    def get_rss(url):
        """
        Method of getting data from the RSS feed
        :param url: URL of RSS feed
        :return: Query result
        """
        response = None
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
            })

            if response.status_code != 200:
                raise RequestProblem

        except RequestProblem:
            print_and_exit(f'Error receiving data from the server: {url}\n'
                           f'Check the correctness of the URL address')

        except requests.exceptions.HTTPError as http_err:
            print_and_exit(f'HTTP error occurred: {http_err}')

        except Exception:
            print_and_exit(f'Error fetching the data from URL: {url}\n'
                           f'Check the correctness of the URL address')
        # with open('response.txt', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        return response

    @staticmethod
    def parse_rss(response):
        """
        RSS parsing method
        :param response: Response from RSS feed
        :return: List of Feed name and list of articles
        """
        articles = None
        soup = None
        feed = None
        if isinstance(response, requests.Response):
            response = response.text
        try:
            soup = BeautifulSoup(response, 'xml')

            if not soup.find('rss'):
                raise NotRSSException

        except NotRSSException:
            print_and_exit('There are not RSS feed link\n'
                           'Check the correctness of the URL address')

        except Exception:
            print_and_exit('Could not parse the rss')

        try:
            feed = soup.find('channel').find('title').text
            articles = soup.findAll('item')

            if articles is None or articles == []:
                raise NoItemsException
        except NoItemsException:
            print_and_exit('There are no items in RSS. Check the correctness of the URL address   ')

        except AttributeError:
            print_and_exit('Incorrect RSS structure, missing channel title tag')

        return [feed, articles]

    @staticmethod
    def get_tags(articles):
        """
        Method gets a list of tags in articles
        :param articles: List of articles
        :return: List of articles tags
        """

        tags = set()
        for a in articles:
            for tag in a.contents:

                if tag == '\n' or tag.name is None:
                    continue
                tags.add(tag.name)

        return tags

    @staticmethod
    def items_to_dict(articles, tags, limit=None, feed=None):
        """
        Method converts a list of articles into a list of articles in dictionary format
        :param articles: List of articles
        :param tags: List of tags in articles
        :param limit: Count of article for display
        :param feed: Feed name
        :return:
        """
        articles_dicts = []
        for a in articles[:limit]:

            item_to_dict = {
                "Feed": '',
                "Title": '',
                "Date": '',
                "Link": '',
                "Description": '',
                "Media": path.join(path.abspath(path.dirname(__file__)), 'templates', 'NoImage.jpg'),
                'Url': '',
                'LocalImgLink': path.join(path.abspath(path.dirname(__file__)), 'templates', 'NoImage.jpg')
            }
            for tag in tags:
                if tag.lower() in keys_dict.keys():
                    new_tag = keys_dict[tag.lower()]
                else:
                    continue
                try:
                    if a.find(tag):
                        res = ReadRss.formatdata(str(a.find(tag).text))
                        text = res[0]
                        if 'href' in a.find(tag).attrs:
                            item_to_dict[new_tag] = a.find(tag)['href']
                        elif 'url' in a.find(tag).attrs:
                            item_to_dict[new_tag] = a.find(tag)['url']
                        elif tag == 'link':
                            item_to_dict[new_tag] = a.find(tag).text.replace('\n', '').replace('\t', '')
                        elif 'type' in a.find(tag).attrs and a.find(tag)['type'] == 'image/jpeg':
                            item_to_dict[new_tag] = a.find(tag)['type']
                        elif res[1]:
                            item_to_dict['Media'] = res[1]

                    else:
                        text = None

                    if text is not None and text != '':
                        if tag.lower() == 'pubdate':

                            item_to_dict[new_tag] = parse(text).date().strftime('%Y.%m.%d')
                        else:
                            item_to_dict[new_tag] = text


                    item_to_dict['Feed'] = feed
                except AttributeError:
                    print(f'Could not find tag "{tag}" in item. Skip it.')

            articles_dicts.append(item_to_dict)
        # with open('articles_in_json.txt', 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(articles_dicts, ensure_ascii=False))
        return articles_dicts

    def print_data(self, colorized=False):
        """Method of printing data to the command line"""
        title_color = ''

        value_color = ''
        if colorized:
            title_color = Fore.GREEN

            value_color = Fore.CYAN

        for item in self.articles_dicts:

            for key in article_tags:

                print(title_color + f'{key}: ', value_color + item.get(key, ''))

            print('-' * 60)

    def print_json(self, colorized=False):
        """Method of printing data to the command line in JSON format"""
        json_data = json.dumps(self.articles_dicts,sort_keys=True, indent=4, ensure_ascii=False)

        if colorized:
            print(highlight(json_data, JsonLexer(), TerminalFormatter()))
        else:
            print(json_data)

    @staticmethod
    def formatdata(data):
        result = data.replace('\n', '').replace('\t', '').replace('<![CDATA[', '').replace(']]>', '').strip()
        result = get_text_from_html(result)

        return result


def run():
    """The main function that runs the program"""
    try:
        namespace = parse_cli_args()


    except Exception as e:
        print('You have specified an invalid command line argument value.')
        print(e)
        sys.exit()

    if namespace.clear_cache:
        clear_db()
        print_and_exit('Data from cache DB deleted.')

    if namespace.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(asctime)s - %(message)s")

    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(asctime)s - %(message)s")


    if namespace.date:
        namespace.date = parse(namespace.date).date().strftime('%Y.%m.%d')
        local = True

    else:
        local = False
    feed = ReadRss(remove_quots(namespace.source), namespace.limit, namespace.date)

    if namespace.json:
        feed.print_json(namespace.colorize)
    else:
        feed.print_data(namespace.colorize)
    if not namespace.date:
        with DataConn() as conn:
            bar = Bar('Processing load articles', max=len(feed.articles_dicts))
            for article in feed.articles_dicts:
                entry = conn.execute('select * from news WHERE (Title=? and Date=?  and Url=?)',
                                     [article.get('Title'), article.get('Date'),
                                      article.get('Url', remove_quots(namespace.source))]).fetchone()

                if entry is None:
                    max_id = conn.execute('select max(id) from news').fetchone()
                    if max_id is None:
                        max_id = 0
                    else:
                        max_id = max_id[0]

                    try:
                        image = requests.get(article.get('Media')).content
                        local_link = get_file_local_path(article.get('Media'))
                        with open(local_link, "wb") as f:
                            f.write(image)

                    except Exception:
                        local_link = path.join(path.abspath(path.dirname(__file__)), 'templates', 'NoImage.jpg')

                    conn.execute(
                        'insert into news(Feed, Title, Link, Date, Description, Media, Url, LocalImgLink) '
                        'values (?, ?, ?, ?, ?, ?, ?, ?)',
                        [article.get('Feed'), article.get('Title'), article.get('Link'), article.get('Date'),
                         article.get('Description'), article.get('Media'), remove_quots(namespace.source), local_link])

                bar.next()
            bar.finish()

            conn.commit()
    if namespace.to_html:

        try:
            if path.isabs(namespace.to_html) and path.isdir(namespace.to_html):
                save_to_html(convert_to_html(feed.articles_dicts, local), namespace.to_html)
            else:
                raise IncorrectPath
        except IncorrectPath:
            print_and_exit('Incorrect path to save file.')

        except PermissionError:
            print_and_exit('You do not have write access to the specified directory.')

    if namespace.to_pdf:

        try:
            if path.isabs(namespace.to_pdf) and path.isdir(namespace.to_pdf):
                save_to_pdf(feed.articles_dicts, namespace.to_pdf, local)
            else:
                raise IncorrectPath
        except IncorrectPath:
            print_and_exit('Incorrect path to save file.')

        except PermissionError:
            print_and_exit('You do not have write access to the specified directory.')


if __name__ == '__main__':
    run()
