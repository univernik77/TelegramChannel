import argparse
from pathlib import Path

import requests
from environs import Env

from split_text_util import split_text


def fetch_apod(url, path, count):
    env = Env()
    params = {
        'api_key': env('API_KEY'),
        'count': count,
        'thumbs': False
    }

    env.read_env()
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    response_url = requests.get(url, params=params)
    response_url.raise_for_status()
    apod_images = response_url.json()
    for number_image, image in enumerate(apod_images[:count]):
        response_image = requests.get(image['url'])
        response_image.raise_for_status()
        with open(f"{path}/nasa_apod_{number_image}"
                  f"{split_text(image['url'])}", 'wb') as file:
            file.write(response_image.content)


def main():
    env = Env()
    env.read_env()
    apod_url = 'https://api.nasa.gov/planetary/apod'
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

    try:
        fetch_apod(apod_url, path_to_file, input_amount)
    except requests.exceptions.HTTPError:
        print('Вы ввели неверный токен.')


if __name__ == '__main__':
    main()
