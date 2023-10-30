import requests
from pathlib import Path


def download_picture(url, path):

    Path(path.split('/')[0]).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    path_to_file = 'images/hubble.jpeg'
    outer_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    download_picture(outer_url, path_to_file)
