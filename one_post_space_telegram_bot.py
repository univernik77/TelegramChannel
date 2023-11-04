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

    bot = telegram.Bot(token=env('TELEGRAM_TOKEN'))
    try:
        bot.send_document(
            chat_id='@SpaceXNasaPictures',
            document=open(input_path, 'rb'))
    except telegram.error.Unauthorized:
        print('Вы ввели неверный токен.')
    except OSError:
        print('Вы ввели неверный путь к файлу.')


if __name__ == '__main__':
    main()
