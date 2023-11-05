import argparse
from pathlib import Path

import requests
from environs import Env

from read_file_util import open_read
from split_text_util import split_text


def find_launch(url):
    response_picture = requests.get(url)
    response_picture.raise_for_status()
    image_launches = response_picture.json()
    for launch in image_launches.reverse():
        if launch['links']['flickr']['original']:
            return launch['links']['flickr']['original']


def fetch_spacex_last_launch(id_launch, path):
    spacex_url = 'https://api.spacexdata.com/v5/launches/'
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    collected_url = f'{spacex_url}{id_launch}'
    response = requests.get(collected_url)
    response.raise_for_status()
    flickr_images = response.json()['links']['flickr']['original']
    spacex_images = flickr_images if flickr_images else find_launch(spacex_url)

    for pict_number, image in enumerate(spacex_images):
        response_image = requests.get(image)
        response_image.raise_for_status()
        collected_path = f"{path}/spacex_{pict_number}{split_text(image)}"
        open_read(collected_path, response_image.content)


def main():
    env = Env()
    env.read_env()
    path_to_file = env('PATH_TO_IMAGES', default='images')

    parser = argparse.ArgumentParser(
        description='Создает папку и загружает фотографии с запусков SpaceX'
    )
    parser.add_argument('id', help='Введите id запуска')
    input_id = parser.parse_args().id

    fetch_spacex_last_launch(input_id, path_to_file)


if __name__ == '__main__':
    main()
