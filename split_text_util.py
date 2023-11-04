from os.path import splitext, split
from urllib.parse import urlsplit, unquote


def split_text(url):
    parsed_url_unquote = unquote(url)
    parsed_url = urlsplit(parsed_url_unquote)
    split_parsed_url = split(parsed_url.path)[1]
    extension = splitext(split_parsed_url)[1]
    return extension
