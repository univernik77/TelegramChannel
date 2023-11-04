import argparse
from pathlib import Path

import requests
from environs import Env

from split_text_util import split_text


def fetch_spacex_last_launch(id_launch, path):
    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    response_url = requests.get(
        f'https://api.spacexdata.com/v5/launches/{id_launch}'
    )
    response_url.raise_for_status()
    spacex_images = response_url.json()['links']['flickr']['original']
    if not spacex_images:
        response_picture = requests.get(
            'https://api.spacexdata.com/v5/launches'
        )
        response_picture.raise_for_status()
        image_launches = response_picture.json()
        for launch in image_launches.reverse():
            if launch['links']['flickr']['original']:
                spacex_images = launch['links']['flickr']['original']
                break

    for number_pict, image in enumerate(spacex_images):
        response_image = requests.get(image)
        response_image.raise_for_status()
        with open(f"{path}/spacex_{number_pict}{split_text(image)}",
                  'wb') as file:
            file.write(response_image.content)


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

