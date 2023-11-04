import argparse
import telegram
from environs import Env


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Публикует одну выбранную фотографию в телеграм-канал'
    )
    parser.add_argument('id', help='Введите путь к файлу')
    input_path = parser.parse_args().id

    try:
        bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))
    except telegram.error.InvalidToken:
        print('Вы ввели неверный токен.')
    try:
        bot.send_document(
            chat_id='@SpaceXNasaPictures',
            document=open(input_path, 'rb'))
    except OSError:
        print('Вы ввели неверный путь к файлу.')


if __name__ == '__main__':
    main()
