import argparse
import os
import random
import time

import telegram
from environs import Env


def main():
    env = Env()
    env.read_env()

    bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))
    images = list(os.walk(env('PATH_TO_IMAGES', default='images')))
    list_images = images[0][2]

    parser = argparse.ArgumentParser(
        description='Скачивает лучшие астрономические фотографии дня'
    )
    parser.add_argument(
        'time',
        nargs='?',
        default=14400,
        help='Введите количество фотографий для скачивания',
        type=int
    )
    input_time = parser.parse_args().time

    count = 0
    while True:
        try:
            bot.send_document(
                chat_id='@SpaceXNasaPictures',
                document=open(f'images/{list_images[count]}', 'rb'))
        except telegram.error.Unauthorized:
            print('Вы ввели неверный токен.')
        except OSError:
            print('Вы ввели неверный путь к файлу.')
        count += 1
        time.sleep(input_time)
        if count == len(list_images)-1:
            count = 0
            random.shuffle(list_images)


if __name__ == '__main__':
    main()