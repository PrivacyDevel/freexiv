#!/usr/bin/env python3

import urllib.parse
import math
import re

import bottle

import api
import config

# from https://s.pximg.net/www/js/build/spa.illust.43512305451e699294de.js
emojis_raw = [(101,"normal"),(102,"surprise"),(103,"serious"),(104,"heaven"),(105,"happy"),(106,"excited"),(107,"sing"),(108,"cry"),(201,"normal2"),(202,"shame2"),(203,"love2"),(204,"interesting2"),(205,"blush2"),(206,"fire2"),(207,"angry2"),(208,"shine2"),(209,"panic2"),(301,"normal3"),(302,"satisfaction3"),(303,"surprise3"),(304,"smile3"),(305,"shock3"),(306,"gaze3"),(307,"wink3"),(308,"happy3"),(309,"excited3"),(310,"love3"),(401,"normal4"),(402,"surprise4"),(403,"serious4"),(404,"love4"),(405,"shine4"),(406,"sweat4"),(407,"shame4"),(408,"sleep4"),(501,"heart"),(502,"teardrop"),(503,"star")] 

emojis = { emoji_name: emoji_id for emoji_id, emoji_name in emojis_raw }


def render_header():
    html = '<style>details[open] > summary {display: none;}</style>'
    html += '<a href="/"><h1>freexiv</h1></a><form action="/search"><input name="q"><input type="submit" value="search"></form>'
    return html

def render_illusts_general(illusts):
    html = ''
    for illust in illusts:
        try:
            url = urllib.parse.urlsplit(illust['url'])
            html += f"<a href='/en/artworks/{illust['id']}'><img src='/{url.netloc}{url.path}' loading='lazy' ></a>"
        except KeyError:
            pass

    return html

def render_illusts_user(illusts):
    html = ''
    for illust_id, illust in illusts:
        url = illust['url']
        url_split = urllib.parse.urlsplit(url)
        html += f"<a href='/en/artworks/{illust_id}'><img src='/{url_split.netloc}{url_split.path}'></a>"
    return html

def render_paged_illusts(illusts, render_fun=render_illusts_general):
    num_of_pages = math.ceil(len(illusts) / api.RECOMMENDS_PAGE_SIZE)
    html = render_fun(illusts[:api.RECOMMENDS_PAGE_SIZE])
    for page in range(1, num_of_pages):
        html += '<details><summary>load more</summary><p>'
        html += render_fun(illusts[page * api.RECOMMENDS_PAGE_SIZE: page * api.RECOMMENDS_PAGE_SIZE + api.RECOMMENDS_PAGE_SIZE])

    for page in range(num_of_pages):
        html += '</p></details>'
    return html

def render_user_header(user_id, user_top):
    html = render_header()

    ogp = user_top['body']['extraData']['meta']['ogp']
    illusts = user_top['body']['illusts']

    if len(illusts) > 0:
        for illust_id, illust in illusts.items():
            image_url = illust['profileImageUrl']
            image_split = urllib.parse.urlsplit(image_url)
            html += f"<img src='/{image_split.netloc}{image_split.path}'>"
            break

    html += f"{ogp['title']}<p>{ogp['description']}</p>"
    html += f'<ul><li><a href="/en/users/{user_id}">Home</a></li><li><a href="/en/users/{user_id}/bookmarks/artworks">Bookmarks</a></li></ul>'
    return html

def render_pager(p, max_p):
    html = '<div>'

    if p > 1:
        html += '<a href="?p=1"><<</a> '
        html += f'<a href="?p={p - 1}"><</a> '

    lowest = max(p - 3, 1)
    highest = min(lowest + 6, max_p)
    if max_p > 6 and highest - lowest < 6:
        lowest = highest - 6

    for i in range(highest - lowest + 1):
        cur = lowest + i
        html += f'<a href="?p={cur}">{cur}</a> '

    if p < max_p:
        html += f'<a href="?p={p + 1}">></a> '
        html += f'<a href="?p={max_p}">>></a>'
    html += '</div>'
    return html



@bottle.get('/')
def landing():
    html = render_header()
    landing_page = api.fetch_landing_page().json()
    html += render_paged_illusts(landing_page['body']['thumbnails']['illust'])
    return html

@bottle.get('/en/artworks/<illust_id:int>')
def artworks(illust_id):
    html = render_header()
    pages = api.fetch_illust_pages(illust_id).json()
    for page in pages['body']:

        regular_url = page['urls']['regular']
        regular_url_split = urllib.parse.urlsplit(regular_url)

        original_url = page['urls']['original']
        original_url_split = urllib.parse.urlsplit(original_url)

        html += f'<a href="/{original_url_split.netloc}{original_url_split.path}"><img src="/{regular_url_split.netloc}{regular_url_split.path}"></a>'

    illust = api.fetch_illust(illust_id).json()['body']
    html += f"<h1>{illust['illustTitle']}</h1>"
    html += f"<p>{illust['description']}</p>"
    html += f"<a href='/en/users/{illust['userId']}'>{illust['userName']}</a>"
    html += f"<h2>Comments</h2>"

    comments = api.fetch_comments(illust_id).json()
    for comment in comments['body']['comments']:
        img = comment['img']
        img_split = urllib.parse.urlsplit(img)
        html += f"<div><a href='/en/users/{comment['userId']}'><img src='/{img_split.netloc}{img_split.path}'>{comment['userName']}</a>: "
        if len(comment['comment']) != 0:

            def replacer(matchobj):
                key = matchobj.group(1)
                if key in emojis:
                    return f'<img src="/s.pximg.net/common/images/emoji/{emojis[key]}.png">'
                else:
                    return key

            comment = re.sub('\(([^)]+)\)', replacer, comment['comment'])
            html += f"{comment}"
        else:
            html += f"<img src='/s.pximg.net/common/images/stamp/generated-stamps/{comment['stampId']}_s.jpg'>"

        html += "</div>"


    recommends = api.fetch_illust_recommends_init(illust_id, api.MAX_RECOMMENDS_PAGE_SIZE).json()
    html += "<h2>Recommended</h2>"
    html += render_paged_illusts(recommends['body']['illusts'])

    return html

@bottle.get('/en/users/<user_id:int>')
def user(user_id):

    user_top = api.fetch_user_top(user_id).json()
    user_all = api.fetch_user_all(user_id).json()

    html = render_user_header(user_id, user_top)

    illusts = user_top['body']['illusts']

    if len(illusts) > 0:
        if len(illusts.items()) == len(user_all['body']['illusts'].items()):
            html += render_paged_illusts(list(illusts.items()), render_illusts_user)
        else:
            illust_ids = list(user_all['body']['illusts'].keys())
            max_num_of_ids_per_page = 100
            illusts = {}
            for page in range(math.ceil(len(illust_ids) / max_num_of_ids_per_page)):
                illusts |= api.fetch_user_illusts(user_id, illust_ids[page * max_num_of_ids_per_page: page * max_num_of_ids_per_page + max_num_of_ids_per_page]).json()
            html += render_paged_illusts(list(illusts['body']['works'].items()), render_illusts_user)
    return html

@bottle.get('/en/users/<user_id:int>/bookmarks/artworks')
def user_bookmarks(user_id):

    p = int(bottle.request.params.get('p', default=1))
    items_per_page = 48

    user_top = api.fetch_user_top(user_id).json()
    bookmarks = api.fetch_user_bookmarks(user_id, (p - 1) * items_per_page, items_per_page).json()

    html = render_user_header(user_id, user_top)

    max_p = math.ceil(bookmarks['body']['total'] / items_per_page)
    html += render_pager(p, max_p)

    illusts = bookmarks['body']['works']
    html += render_illusts_general(illusts)

    html += render_pager(p, max_p)

    return html

@bottle.get('/user_banner/<user_id:int>')
def user_banner(user_id):
    resp = api.fetch_user_banner(user_id)
    bottle.response.set_header('content-type', resp.headers.get('content-type'))
    return resp.content

@bottle.get('/search')
def search():
    html = render_header()
    search_term = bottle.request.query.q
    search_term_encoded = urllib.parse.quote(search_term)
    search_results = api.fetch_search_results(search_term).json()
    illusts = search_results['body']['illustManga']['data']
    html += render_paged_illusts(illusts)
    return html

bottle.run(host=config.BIND_ADDRESS, server=config.SERVER, port=config.BIND_PORT)
