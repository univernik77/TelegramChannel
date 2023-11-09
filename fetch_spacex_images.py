import argparse
from pathlib import Path

from environs import Env

from support_util import split_url, read_file, get_response


def get_flickr_image(url, input_id):
    response = get_response(f'{url}{input_id}')
    return response.json()['links']['flickr']['original']


def check_launch_images(url, input_id):
    flickr_images = get_flickr_image(url, input_id)
    if not flickr_images:
        response_launches = get_response(url)
        images_launches = response_launches.json()
        for launch in reversed(images_launches):
            if launch['links']['flickr']['original']:
                return launch['id']
    return input_id


def fetch_spacex_last_launch(url, input_id, path):

    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)

    spacex_images = get_flickr_image(url, input_id)
    for image_number, image in enumerate(spacex_images):
        response_image = get_response(image)
        file_ext = split_url(image)
        collected_path = f"{path}/spacex_{image_number}{file_ext}"
        read_file(collected_path, response_image.content)


def main():
    env = Env()
    env.read_env()
    path_to_file = env('PATH_TO_IMAGES', default='images')
    spacex_url = 'https://api.spacexdata.com/v5/launches/'

    parser = argparse.ArgumentParser(
        description='Создает папку и загружает фотографии с запусков SpaceX'
    )
    parser.add_argument('id', help='Введите id запуска')
    input_id = parser.parse_args().id

    check_launch_id = check_launch_images(spacex_url, input_id)
    fetch_spacex_last_launch(spacex_url, check_launch_id, path_to_file)


if __name__ == '__main__':
    main()
