from os.path import splitext, split
from urllib.parse import urlsplit, unquote

import requests


def split_url(url):
    parsed_url_unquote = unquote(url)
    parsed_url = urlsplit(parsed_url_unquote)
    split_parsed_url = split(parsed_url.path)[1]
    extension = splitext(split_parsed_url)[1]
    return extension


def read_file(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)


def get_response(url, params=''):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response
