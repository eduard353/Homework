import unittest
from os import path
from unittest.mock import patch
import json
from bs4 import BeautifulSoup
from rss_parser import ReadRss, print_and_exit, parse_cli_args, remove_quots, get_text_from_html
from parser_exceptions import *


class TestReadRss(unittest.TestCase):

    def setUp(self) -> None:
        with open(path.join(path.abspath(path.dirname(__file__)), 'test_data', 'response.txt'), 'r', encoding='utf-8') as f:
            response = f.read()
        soup = BeautifulSoup(response, 'xml')

        self.articles = soup.findAll('item')
        self.feed = soup.find('channel').find('title').text
        self.tags = {'guid', 'author', 'description', 'enclosure', 'category', 'link', 'pubDate', 'title'}
        self.more_tags = {'guid', 'test_tag', 'author', 'description', 'enclosure', 'category', 'link', 'pubDate',
                          'title'}

    def test_remove_quots(self):

        dq_string = '"String with double quots"'
        no_dq_string = 'String with double quots'
        q_string = "'String with quots'"
        no_q_string = "String with quots"

        self.assertEqual(remove_quots(dq_string), no_dq_string)
        self.assertEqual(remove_quots(q_string), no_q_string)

    def test_get_text_from_html(self):
        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'html.txt'), 'r', encoding='utf-8') as f:
            html = f.read()
        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'only_text_html.txt'), 'r', encoding='utf-8') as f:
            only_text_html = f.read()
        self.assertEqual(get_text_from_html(html), only_text_html)

    def test_print_exit(self):
        with self.assertRaises(SystemExit):
            print_and_exit('test')

    def test_parse_cli(self):
        parser = parse_cli_args(['--limit', '2', '--verbose', '--json', 'http://lenta.ru/l/r/EX/import.rss'])
        self.assertTrue(parser.json)
        self.assertTrue(parser.verbose)
        self.assertTrue(parser.limit)

        self.assertEqual(parser.limit, 2)
        self.assertTrue(parser.source)
        self.assertEqual(parser.source, 'http://lenta.ru/l/r/EX/import.rss')

    @patch('requests.get')
    def test_get_rss(self, mock_get):
        mock_get.return_value.status_code = 200
        response = ReadRss.get_rss('http://lenta.ru/l/r/EX/import.rss')

        self.assertIsNotNone(response)

    def test_parse_rss(self):
        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'response.txt'), 'r', encoding='utf-8') as f:
            response = f.read()

        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'bad_response_no_channel.txt'), 'r') as f:
            no_channel_response = f.read()

        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'bad_response_no_items.txt'), 'r') as f:
            no_items_response = f.read()
        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'bad_response_no_rss.txt'), 'r') as f:
            no_rss_response = f.read()
        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'bad_response.txt'), 'r') as f:
            bad_response = f.read()

        result = ReadRss.parse_rss(response)
        self.assertIsInstance(result, list)

        with self.assertRaises((AttributeError, SystemExit)):
            ReadRss.parse_rss(no_channel_response)

        with self.assertRaises((NoItemsException, SystemExit)):
            ReadRss.parse_rss(no_items_response)

        with self.assertRaises((NotRSSException, SystemExit)):
            ReadRss.parse_rss(no_rss_response)

        with self.assertRaises((Exception, SystemExit)):
            ReadRss.parse_rss(bad_response)

    def test_get_tags(self):
        # print(self.articles)
        result = ReadRss.get_tags(self.articles)
        self.assertIsInstance(result, set)
        self.assertEqual(result, self.tags)

    def test_items_to_dict(self):
        result = ReadRss.items_to_dict(self.articles, self.tags, feed=self.feed)
        self.assertIsInstance(result, list)

        print(result[0])

        with open(path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'articles_in_json.txt'), 'r', encoding='utf-8') as f:
            articles_dicts = json.loads(f.read())
        print(articles_dicts[0])

        self.assertListEqual(result, articles_dicts)

    def test_get_news_from_db(self):
        test_db = path.join(path.abspath(path.dirname(__file__)),
                            'test_data', 'rss_cache.db')
        result = ReadRss.get_news_from_db('2022.06.27', 'http://lenta.ru/l/r/EX/import.rss', 2, test_db)

        self.assertIsInstance(result, list)