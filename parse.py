from bs4 import BeautifulSoup as BS
import requests
from pprint import pprint as print
import arrow
import re
from fuzzywuzzy import fuzz, process

def get_html_tree(link):
    page = requests.get(link)
    return BS(page.content, "lxml")


class IGG:
    url = 'https://igg-games.com'

    def __init__(self):
        self.soup = get_html_tree(IGG.url)
        self.games_link = self.soup.select_one(".uk-nav-default > li:nth-child(7) > a:nth-child(1)")['href']

    @property
    def featured_games(self):
        selector = ".n2-ss-slide"
        elements = self.soup.select(selector)
        return [e['data-href'] for e in elements]

    @property
    def all_games(self):
        soup = get_html_tree(self.games_link)
        games = soup.select('.uk-margin-medium-top > ul > li > a')
        return [
            {
                "name": game.text,
                "href": game['href']
            } for game in games
        ]

    def search(self, string, limit=5):
        all_games = self.all_games
        matches = process.extract(string, [game['href'] for game in self.all_games], limit=limit)
        return [Game(match[0]) for match in matches]


class Game:

    def __init__(self, href):
        self.soup = get_html_tree(href)
        self.article = self.soup.select_one('article')

    @property
    def title(self):
        return self.soup.select_one('h1')

    @property
    def download_links(self):
        links = self.article.find_all('a', href=re.compile("http://bluemediafiles.com/.*?"))
        return [
            'http'+link['href'].split('url=')[1] for link in links
        ]

    @property
    def description(self):
        return self.article.text

    @property
    def images(self):
        images = self.article.select('img')
        return [img['src'] for img in images if 'igg-games' in img['src']]

    @property
    def tags(self):
        tags = self.article.find_all('a',{'rel': 'category'})
        return [{
            'name': tag.text,
            'href': tag['href']
        } for tag in tags]

    @property
    def published_at(self):
        stamp = self.article.select_one('time')['datetime']
        return [arrow.get(stamp), arrow.get(stamp).humanize()]

    @property
    def updates(self):
        updates = self.article.select('.uk-label-success')
        print(updates)
        parsed = []
        for update in updates:
            print('update')
            name = update.text
            links = update.parent.find_next('p')
            parsed.append({
                'version': name,
                'links': [href['href'] for href in links.find_all('a')]
            })
        return parsed


igg = IGG()
game_href = igg.all_games[16602]['href']
game = Game(game_href)
print(game.title.text)
# print(game.tags)
games = igg.search('sims')

for g in games:
    print(g.title)
    print(g.download_links)
