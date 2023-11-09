import argparse
from pathlib import Path

from environs import Env

from support_util import split_url, read_file, get_response


def fetch_apod(key, path, count):
    params = {
        'api_key': key,
        'count': count,
        'thumbs': False
    }
    apod_url = 'https://api.nasa.gov/planetary/apod'

    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    response_images = get_response(apod_url, params)
    apod_images = response_images.json()
    for image_number, image in enumerate(apod_images[:count]):
        file_ext = split_url(image['url'])
        collected_path = (f"{path}/nasa_apod_{image_number}"
                          f"{file_ext}")
        response_image = get_response(image['url'])
        read_file(collected_path, response_image.content)


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

    fetch_apod(env('NASA_API_KEY'), path_to_file, input_amount)


if __name__ == '__main__':
    main()
