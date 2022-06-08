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
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='RSS URL', default=None)
    parser.add_argument('--version', action='version', version='Version 2.0')
    parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    return parser

class ReadRss:

    def __init__(self, rss_url, headers):

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
        self.articles_dicts = [
            {'title': a.find('title').text, 'link': a.link.next_sibling.replace('\n', '').replace('\t', ''),
             'pubdate': a.find('pubdate').text} for a in self.articles]
        # self.articles_dicts = [
        #     {'title': a.find('title').text, 'link': a.link.next_sibling.replace('\n', '').replace('\t', ''),
        #      'description': a.find('description').text, 'pubdate': a.find('pubdate').text} for a in self.articles]



if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()

    feed = ReadRss(namespace.source.replace("'",''), headers)
    
    print('Feed: ', feed.feed, end='\n\n')

    # for item in feed.articles_dicts:
    #     print('Title: ', item['title'])
    #     print('Date: ', item['pubdate'])
    #     print('Link: ', item['link'], end='\n\n')

    for item in feed.articles:

        print('item - ',item)
        print('item contents - ', item.contents)
        for x in item.contents:
            if x == '\n':
                continue
            print(x, ' - ', x.name)

    # print(feed.soup)
    # with open('soup1.txt', 'w') as f:
    #     f.write(str(feed.soup))
