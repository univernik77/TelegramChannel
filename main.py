from urllib.parse import urlsplit, unquote
from os.path import splitext, split
from pathlib import Path

import requests


def split_text(url):
    parsed_url_unquote = unquote(url)
    parsed_url = urlsplit(parsed_url_unquote)
    split_parsed_url = split(parsed_url.path)[1]
    return splitext(split_parsed_url)[1]


def fetch_spacex_last_launch(url, path):
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)
    url_response = requests.get(url)
    url_response.raise_for_status()
    spacex_pictures = url_response.json()['links']['flickr']['original']
    for pict_number, picture in enumerate(spacex_pictures):
        pict_response = requests.get(picture)
        pict_response.raise_for_status()
        with open(f"{path.split('.')[0]}{pict_number}.jpg", 'wb') as file:
            file.write(pict_response.content)


def fetch_nasa_apod(url, path):
    params = {'api_key': 'jaQVVYNcDTPMx0mlBFQe0cLIocGRH8RH3vbuQtDA',
              'count': 30}
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)
    url_response = requests.get(url, params=params)
    url_response.raise_for_status()
    nasa_pictures = url_response.json()
    for pict_number, picture in enumerate(nasa_pictures):
        pict_response = requests.get(picture['url'])
        pict_response.raise_for_status()
        with open(f"{path.split('.')[0]}{pict_number}.{split_text(picture['url'])}", 'wb') as file:
            file.write(pict_response.content)


def fetch_nasa_epic(url, path):
    params = {'api_key': 'jaQVVYNcDTPMx0mlBFQe0cLIocGRH8RH3vbuQtDA'}
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)
    url_response = requests.get(url, params=params)
    url_response.raise_for_status()
    nasa_pictures = url_response.json()
    for pict_number, picture in enumerate(nasa_pictures):
        split_date = picture['date'].split(' ')[0].split('-')
        join_date = '/'.join(split_date)
        pict_response = requests.get(
            f"https://api.nasa.gov/EPIC/archive/natural/{join_date}/png/{picture['image']}.png", params=params)
        pict_response.raise_for_status()
        with open(f"{path.split('.')[0]}{pict_number}.{'png'}", 'wb') as file:
            file.write(pict_response.content)


if __name__ == '__main__':
    path_to_file = 'spacex_images/space_.jpg'
    spaceX_url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    nasa_apod_url = 'https://api.nasa.gov/planetary/apod'
    path_to_file_nasa_apod = 'nasa_images/nasa_apod.jpg'
    nasa_epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    path_to_file_nasa_epic = 'nasa_epic_images/nasa_apod_.jpg'
    fetch_nasa_epic(nasa_epic_url, path_to_file_nasa_epic)
    fetch_spacex_last_launch(spaceX_url, path_to_file)
    fetch_nasa_apod(nasa_apod_url, path_to_file_nasa_apod)
