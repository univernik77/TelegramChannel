import argparse
from datetime import datetime as dt
from pathlib import Path

import requests
from environs import Env

from read_file_util import open_read


def fetch_nasa_epic(key, path, count):
    params = {'api_key': key}
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'

    Path(path).mkdir(parents=True, exist_ok=True)

    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    epic_images = response.json()
    for image_number, image in enumerate(epic_images[:count]):
        image_date = dt.strptime(image['date'], '%Y-%m-%d %H:%M:%S')
        str_image_date = dt.strftime(image_date, '%Y/%m/%d')
        collected_url = (f"https://api.nasa.gov/EPIC/archive/natural/"
                         f"{str_image_date}/png/{image['image']}.png")
        response_image = requests.get(collected_url, params=params)
        response_image.raise_for_status()
        collected_path = f'{path}/nasa_epic_{image_number}.png'
        open_read(collected_path, response_image.content)


def main():
    env = Env()
    env.read_env()
    path_to_file = env('PATH_TO_IMAGES', default='images')

    parser = argparse.ArgumentParser(
        description='Скачивает эпические фотографии земли, '
                    'согласно введенной дате')
    parser.add_argument(
        'count',
        nargs='?',
        default=10,
        help='Введите количество фотографий для скачивания',
        type=int
    )
    input_count = parser.parse_args().count

    fetch_nasa_epic(env('API_KEY'), path_to_file, input_count)


if __name__ == '__main__':
    main()
