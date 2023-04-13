#!/usr/bin/env python3

import urllib.parse

import bottle

import api

def render_header():
    return '<form action="/search"><input name="q"><input type="submit" value="search"></form>'

def render_illusts(illusts):
    html = ''
    for illust in illusts:
        try:
            url_encoded = urllib.parse.quote(illust['url'])
            html += f"<a href='/en/artworks/{illust['id']}'><img src='/pximg/{url_encoded}'></a>"
        except KeyError:
            pass
    return html

@bottle.get('/')
def landing():
    return render_header()

@bottle.get('/en/artworks/<illust_id:int>')
def artworks(illust_id):
    html = render_header()
    pages = api.fetch_illust_pages(illust_id).json()
    for page in pages['body']:

        regular_url = page['urls']['small']
        regular_url_encoded = urllib.parse.quote(regular_url)

        original_url = page['urls']['original']
        original_url_encoded = urllib.parse.quote(original_url)

        html += f'<a href="/pximg/{original_url_encoded}"><img src="/pximg/{regular_url_encoded}"></a>'

    illust = api.fetch_illust(illust_id).json()['body']
    html += f"<h1>{illust['illustTitle']}</h1>"
    html += f"<p>{illust['description']}</p>"
    html += f"<a href='/en/users/{illust['userId']}'>{illust['userName']}</a>"
    html += f"<h2>Comments</h2>"

    comments = api.fetch_comments(illust_id).json()
    for comment in comments['body']['comments']:
        img = comment['img']
        img_encoded = urllib.parse.quote(img)
        html += f"<div><a href='/en/users/{comment['userId']}'><img src='/pximg/{img_encoded}'>{comment['userName']}</a>: {comment['comment']}</div>"

    recommends = api.fetch_illust_recommends(illust_id).json()
    html += "<h2>Recommended</h2>"
    html += render_illusts(recommends['body']['illusts'])

    return html

@bottle.get('/en/users/<user_id:int>')
def users(user_id):
    html = render_header()

#    user = api.fetch_user_top(user_id).json()
#    ogp = user['body']['extraData']['meta']['ogp']
#    banner_image = ogp['image']
#    banner_image_query = urllib.parse.urlsplit(banner_image).query
#    banner_image_id = urllib.parse.parse_qs(banner_image_query)['id'][0]
#    return f"<img src='/profile_pic/{banner_image_id}'>{ogp['title']}<p>{ogp['description']}</p>"

    user = api.fetch_user_top(user_id).json()
    ogp = user['body']['extraData']['meta']['ogp']
    illusts = user['body']['illusts']

    if len(illusts) > 0:
        for illust_id, illust in illusts.items():
            image_url = illust['profileImageUrl']
            image_encoded = urllib.parse.quote(image_url)
            html += f"<img src='/pximg/{image_encoded}'>"
            break

    html += f"{ogp['title']}<p>{ogp['description']}</p>"

    if len(illusts) > 0:
        for illust_id, illust in illusts.items():
            url = illust['url']
            url_encoded = urllib.parse.quote(url)
            html += f"<a href='/en/artworks/{illust_id}'><img src='/pximg/{url_encoded}'</a>"
    return html

@bottle.get('/pximg/<path:path>')
def pximg(path):
    resp = api.fetch_pximg(urllib.parse.unquote(path))
    bottle.response.set_header('content-type', resp.headers.get('content-type'))
    return resp.content

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
    html += render_illusts(illusts)
    return html

bottle.run(host='0.0.0.0')
