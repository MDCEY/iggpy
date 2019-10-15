__version__ = '0.1.0'

from bs4 import BeautifulSoup as BS
import requests
import arrow
import re
from urllib.parse import urlparse
import hug

api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api, max_age=10))

def get_html_tree(link):
    page = requests.get(link)
    return BS(page.content, "lxml")


@hug.get('/games')
def fetch_all_games_list(cors: hug.directives.cors="*"):
    soup = get_html_tree('https://igg-games.com')
    all_games_link = soup.select_one('.uk-nav-default > li:nth-child(7) > a:nth-child(1)')['href']
    soup = get_html_tree(all_games_link)
    games = soup.select('.uk-margin-medium-top > ul > li > a')
    return [
        {
            "name": game.text,
            "href": '/game' + urlparse(game['href']).path
        } for game in games
    ]


@hug.get('/recent')
def get_recent_activity():
    soup = get_html_tree('https://igg-games.com')
    updates_link = soup.select_one(".uk-nav-default > li:nth-child(8) > a:nth-child(1)")['href']
    games = get_html_tree(updates_link)
    dates = games.select('.uk-text-meta')
    game_updates = []
    for d in dates:
        text = d.text
        date = text.split('(')[1][:-1]
        print(f'Fetching games for {d}')
        for link in d.parent.find_next('ul').find_all('li'):
            print(f'found: {link}')
            item = {
                'date': arrow.get(date, 'MMMM DD, YYYY').format('YYYY-MM-DD'),
                'href': '/game' + urlparse(link.find('a')['href']).path,
                'name': link.find('a').text,
                'type': link.find('span').text
            }
            game_updates.append(item)
    return game_updates


@hug.get('/featured')
def get_featured():
    soup = get_html_tree('https://igg-games.com')
    selector = ".n2-ss-slide"
    elements = soup.select(selector)
    return [urlparse(e['data-href']).path for e in elements]


@hug.get('/game/{path}')
def get_game(path, cors: hug.directives.cors="*"):
    # Pull data for each game. return as json
    soup = get_html_tree(f'https://igg-games.com/{path}')
    article = soup.select_one('article')
    if article:
        print(article)
    title = soup.find('h1').text

    links = article.find_all('a', href=re.compile("http://bluemediafiles.com/.*?"))
    download_links = ['http' + link['href'].split('url=')[1][:-1] for link in links]
    game_description = article.text

    images_selection = article.select('img')
    game_images = [img['src'] for img in images_selection if 'igg-games' in img['src']]

    tag_selection = article.find_all('a', {'rel': 'category'})
    tags = [{
             'name': tag.text,
             'href': tag['href']
         } for tag in tag_selection]

    published_at_selector = article.select_one('time')['datetime']
    published_at = arrow.get(published_at_selector).humanize()

    updates_selector = article.select('.uk-label-success')
    updates = []
    for update in updates_selector:
        name = update.text
        links = update.parent.find_next('p')
        updates.append({
            'version': name,
            'links': [href['href'] for href in links.find_all('a')]
        })

    return {
        'header': title,
        'publish_date': published_at,
        'tags': tags,
        'description': game_description,
        'images': game_images,
        'downloads': download_links,
        'updates': updates
    }


#     @property
#     def updates(self):
#         updates = self.article.select('.uk-label-success')
#         print(updates)
#         parsed = []
#         for update in updates:
#             print('update')
#             name = update.text
#             links = update.parent.find_next('p')
#             parsed.append({
#                 'version': name,
#                 'links': [href['href'] for href in links.find_all('a')]
#             })
#         return parsed
#
#
# igg = IGG()
# # print(igg.updates())
# res = igg.search('Kenshi')
# for r in res:
#     print(r.title)
#     print(r.download_links)
#     print(r.updates)
