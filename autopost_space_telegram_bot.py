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
    telegram_images = images[0][2]

    parser = argparse.ArgumentParser(
        description='Публикует фотографии в Телеграм-канал'
    )
    parser.add_argument(
        'time',
        nargs='?',
        default=14400,
        help='Введите интервал между публикациями в секундах',
        type=int
    )
    input_time = parser.parse_args().time

    count = 0
    while True:
        try:
            collected_path = f'images/{telegram_images[count]}'
            with open(collected_path, 'rb') as file:
                bot.send_document(
                    chat_id=env('CHAT_ID'),
                    document=file)
        except telegram.error.Unauthorized:
            print('Вы ввели неверный токен.')
        except OSError:
            print('Вы ввели неверный путь к файлу.')
        count += 1
        time.sleep(input_time)
        if count == len(telegram_images) - 1:
            count = 0
            random.shuffle(telegram_images)


if __name__ == '__main__':
    main()
