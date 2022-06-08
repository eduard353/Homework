import argparse
from bs4 import BeautifulSoup
import requests
import logging

headers = {
    'User-Agent': 'your-user-agent-here'
}

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def createParser():
    """
    Функция для парсинга параметров командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version='Version 2.0')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    return parser


class ReadRss:
    """
    Класс парсера RSS ленты
    """
    def __init__(self, rss_url, headers):
        self.req_tags = ['title', 'pubdate', 'link']
        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:
            self.soup = BeautifulSoup(self.r.text, 'lxml')
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

        for a in self.articles:
            print(a)
            item_to_dict = dict()
            for tag in self.tags:
                try:
                    text = a.find(tag).text

                    if text is not None and text != '':
                        item_to_dict[tag] = a.find(tag).text
                    elif tag == 'link':
                        item_to_dict['link'] = a.find(tag).next_sibling.replace('\n', '').replace('\t', '')
                    elif tag == 'atom:link' and a.find(tag)['href']:
                        item_to_dict['link'] = a.find(tag)['href']

                        # self.dicts.append({t:a.find(t).text for t in self.tags})
                except AttributeError as e:
                    print(f'Could not find tag "{tag}" in item.')
                    print(e)
            self.articles_dicts.append(item_to_dict)


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

    feed = ReadRss(namespace.source.replace("'", ''), headers)

    print('Feed: ', feed.feed, end='\n\n')

    for item in feed.articles_dicts:

        for req_tag in feed.req_tags:
            print(f'{req_tag}: ', item.get(req_tag))
        for nreq_tag in set(feed.tags).difference(set(feed.req_tags)):
            print(f'{nreq_tag}: ', item.get(nreq_tag))
        print('-'*60)



    # print(feed.tags)
    # print(feed.articles_dicts)

