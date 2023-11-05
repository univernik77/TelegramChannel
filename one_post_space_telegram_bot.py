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
        with open(input_path, 'rb') as file:
            bot.send_document(
                chat_id=env('CHAT_ID'),
                document=file)
    except telegram.error.Unauthorized:
        print('Вы ввели неверный токен.')
    except OSError:
        print('Вы ввели неверный путь к файлу.')


if __name__ == '__main__':
    main()
