import urllib.parse

import requests

import config

DEFAULT_RECOMMENDS_PAGE_SIZE = 18
RECOMMENDS_PAGE_SIZE = DEFAULT_RECOMMENDS_PAGE_SIZE * 2
MAX_RECOMMENDS_PAGE_SIZE = 161

def gen_auth_headers():
    return {
        'Cookie': f'PHPSESSID={config.SESSION_ID}',
        'User-Agent': 'Mozilla/5.0'
    }

def fetch_illust_pages(illust_id):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}/pages'
    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_illust(illust_id):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}'
    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_comments(illust_id):
    url = f'https://www.pixiv.net/ajax/illusts/comments/roots?illust_id={illust_id}'
    resp = requests.get(url, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_user_top(user_id):
    url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/top'
    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_user_all(user_id):
    url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/all'
    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp


def fetch_illust_recommends_init(illust_id, limit=RECOMMENDS_PAGE_SIZE):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}/recommend/init?limit={limit}'
    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

#def fetch_illust_recommends_next(ids):
#    url = f'https://www.pixiv.net/ajax/illust/recommend/'
#    resp = requests.get(url, headers=gen_auth_headers(), proxies=config.PROXIES) # needed?
#    resp.raise_for_status()
#    return resp

def fetch_user_banner(user_id):
    resp = requests.get(f'https://embed.pixiv.net/user_profile.php?id={user_id}', proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_search_results(search_term):
    search_term_encoded = urllib.parse.quote(search_term)
    resp = requests.get(f'https://www.pixiv.net/ajax/search/artworks/{search_term_encoded}', headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_landing_page():
    resp = requests.get(f'https://www.pixiv.net/ajax/top/illust', headers=gen_auth_headers(), proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

