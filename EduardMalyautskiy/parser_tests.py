import unittest
from os import path
from unittest.mock import patch
import json
from bs4 import BeautifulSoup
from rss_parser import ReadRss, print_and_exit, parse_cli_args
from parser_exceptions import *



class TestReadRss(unittest.TestCase):

    def setUp(self) -> None:
        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','response.txt'), 'r', encoding='utf-8') as f:
            response = f.read()
        soup = BeautifulSoup(response, 'xml')

        self.articles = soup.findAll('item')

        self.tags = {'guid', 'author', 'description', 'enclosure', 'category', 'link', 'pubDate', 'title'}
        self.more_tags = {'guid', 'test_tag', 'author', 'description', 'enclosure', 'category', 'link', 'pubDate',
                          'title'}

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
        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','response.txt'), 'r', encoding='utf-8') as f:
            response = f.read()

        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','bad_response_no_channel.txt'), 'r') as f:
            no_channel_response = f.read()

        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','bad_response_no_items.txt'), 'r') as f:
            no_items_response = f.read()
        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','bad_response_no_rss.txt'), 'r') as f:
            no_rss_response = f.read()
        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','bad_response.txt'), 'r') as f:
            bad_response = f.read()

        result = ReadRss.parse_rss(response)
        self.assertIsInstance(result, tuple)

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
        result = ReadRss.items_to_dict(self.articles, self.tags)
        self.assertIsInstance(result, list)
        # print(result)

        with open(path.join(path.abspath(path.dirname(__file__)),'test_data','articles_in_json.txt'), 'r', encoding='utf-8') as f:
            articles_dicts = json.loads(f.read())

        self.assertListEqual(result, articles_dicts)
