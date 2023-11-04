import argparse
from datetime import datetime as dt
from pathlib import Path

import requests
from environs import Env


def fetch_nasa_epic(url, path, count):
    env = Env()
    params = {'api_key': env('API_KEY')}

    env.read_env()
    Path(path).mkdir(parents=True, exist_ok=True)

    response_url = requests.get(url, params=params)
    response_url.raise_for_status()
    epic_images = response_url.json()
    for number_image, image in enumerate(epic_images[:count]):
        image_date = dt.strptime(image['date'], '%Y-%m-%d %H:%M:%S')
        str_image_date = dt.strftime(image_date, '%Y/%m/%d')
        response_image = requests.get(
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{str_image_date}/png/{image['image']}.png",
            params=params
        )
        response_image.raise_for_status()
        with open(f'{path}/nasa_epic_{number_image}.png', 'wb') as file:
            file.write(response_image.content)


def main():
    env = Env()
    env.read_env()

    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
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

    try:
        fetch_nasa_epic(epic_url, path_to_file, input_count)
    except requests.exceptions.HTTPError:
        print('Вы ввели неверный токен.')


if __name__ == '__main__':
    main()
