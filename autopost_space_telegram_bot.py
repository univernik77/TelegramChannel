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
    images = list(os.walk(env('PATH_TO_IMAGE', default='images')))
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

    while True:
        try:
            for image in telegram_images:
                with open(f'images/{image}', 'rb') as file:
                    bot.send_document(
                        chat_id=env('TG_CHAT_ID'),
                        document=file)
        except telegram.error.Unauthorized:
            print('Вы ввели неверный токен.')
        except OSError:
            print('Вы ввели неверный путь к файлу.')
        time.sleep(input_time)
        random.shuffle(telegram_images)


if __name__ == '__main__':
    main()
