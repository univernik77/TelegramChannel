import argparse
from datetime import datetime as dt
from pathlib import Path

from environs import Env

from support_util import read_file, get_response


def fetch_nasa_epic(key, path, count):
    params = {'api_key': key}
    epic_url_natural = 'https://api.nasa.gov/EPIC/archive/natural/'
    epic_url_images = 'https://api.nasa.gov/EPIC/api/natural/images'

    Path(path).mkdir(parents=True, exist_ok=True)

    response_image = get_response(epic_url_images, params)
    epic_images = response_image.json()
    for image_number, image in enumerate(epic_images[:count]):
        image_date = dt.strptime(image['date'], '%Y-%m-%d %H:%M:%S')
        str_image_date = dt.strftime(image_date, '%Y/%m/%d')
        collected_url = (f"{epic_url_natural}"
                         f"{str_image_date}/png/{image['image']}.png")
        collected_path = f'{path}/nasa_epic_{image_number}.png'
        response_image = get_response(collected_url, params)
        read_file(collected_path, response_image.content)


def main():
    env = Env()
    env.read_env()
    path_to_file = env('PATH_TO_IMAGE', default='images')

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

    fetch_nasa_epic(env('NASA_API_KEY'), path_to_file, input_count)


if __name__ == '__main__':
    main()
