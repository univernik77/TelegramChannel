import requests
from pathlib import Path


def download_picture():
    filename = 'hubble.jpeg'
    directory = 'images'
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    Path(directory).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with open(f'{directory}/{filename}', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    download_picture()
