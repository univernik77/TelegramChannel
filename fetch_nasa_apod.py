import argparse
from pathlib import Path

import requests
from environs import Env

from read_file_util import open_read
from split_text_util import split_text


def fetch_apod(key, path, count):
    params = {
        'api_key': key,
        'count': count,
        'thumbs': False
    }
    apod_url = 'https://api.nasa.gov/planetary/apod'

    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    apod_images = response.json()
    for image_number, image in enumerate(apod_images[:count]):
        response_image = requests.get(image['url'])
        response_image.raise_for_status()
        collected_path = (f"{path}/nasa_apod_{image_number}"
                          f"{split_text(image['url'])}")

        open_read(collected_path, response_image.content)


def main():
    env = Env()
    env.read_env()
    path_to_file = env('PATH_TO_IMAGE', default='images')

    parser = argparse.ArgumentParser(
        description='Скачивает лучшие астрономические фотографии дня'
    )
    parser.add_argument(
        'amount',
        nargs='?',
        default=30,
        help='Введите количество фотографий для скачивания',
        type=int
    )
    input_amount = parser.parse_args().amount

    fetch_apod(env('API_KEY'), path_to_file, input_amount)


if __name__ == '__main__':
    main()
