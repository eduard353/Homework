import unittest
from unittest.mock import MagicMock
import sys
import argparse
from bs4 import Tag

from rss_parser import ReadRss, print_and_exit, parse_cli_args



class TestReadRss(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_print_exit(self):
        with self.assertRaises(SystemExit):
            print_and_exit('test')

    def test_parse_cli(self):
        parser = parse_cli_args(['--limit', '2', '--verbose', '--json', 'http://lenta.ru/l/r/EX/import.rss'])
        print(parser)
        self.assertTrue(parser.json)
        self.assertTrue(parser.verbose)
        self.assertTrue(parser.limit)

        self.assertEqual(parser.limit, 2)
        self.assertTrue(parser.source)
        self.assertEqual(parser.source, 'http://lenta.ru/l/r/EX/import.rss')

    def test_get_rss(self):
        ReadRss.get_rss()
