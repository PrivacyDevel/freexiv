import urllib.parse

import requests

import config


class ForbiddenProxyDestException(Exception):
    def __init__(self, netloc):
        super().__init__(netloc)


def fetch_pximg(url):

    netloc = urllib.parse.urlsplit(url).netloc
    if not netloc in ['s.pximg.net', 'i.pximg.net']:
        raise ForbiddenProxyDestException(netloc)

    headers = {
            'Referer': 'https://www.pixiv.net/'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp

def fetch_illust_pages(illust_id):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}/pages'
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(url, headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_illust(illust_id):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}'
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(url, headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_comments(illust_id):
    url = f'https://www.pixiv.net/ajax/illusts/comments/roots?illust_id={illust_id}'
    resp = requests.get(url, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_user_top(user_id):
    url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/top'
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(url, headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_user_all(user_id):
    url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/all'
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(url, headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp


def fetch_illust_recommends(illust_id, limit=18):
    url = f'https://www.pixiv.net/ajax/illust/{illust_id}/recommend/init?limit={limit}'
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(url, headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_user_banner(user_id):
    resp = requests.get(f'https://embed.pixiv.net/user_profile.php?id={user_id}', proxies=config.PROXIES)
    resp.raise_for_status()
    return resp

def fetch_search_results(search_term):
    search_term_encoded = urllib.parse.quote(search_term)
    headers = {
            'Cookie': f'PHPSESSID={config.SESSION_ID}',
            'User-Agent': 'Mozilla/5.0'
    }
    resp = requests.get(f'https://www.pixiv.net/ajax/search/artworks/{search_term_encoded}', headers=headers, proxies=config.PROXIES)
    resp.raise_for_status()
    return resp
