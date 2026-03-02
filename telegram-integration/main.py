#!/usr/bin/env python3
"""Точка входа: отправка текста из файла в Telegram-чат."""

import argparse
import sys

from bot import TelegramClient
from config import get_bot_token, get_chat_id
from text_handler import TextHandler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Отправка текста из .txt файла в приватный Telegram-чат."
    )
    parser.add_argument("file", help="путь к .txt файлу")
    parser.add_argument(
        "--chat-id",
        help="chat_id (переопределяет TELEGRAM_CHAT_ID из .env)",
    )
    args = parser.parse_args()

    token = get_bot_token()
    if not token:
        print("Ошибка: TELEGRAM_BOT_TOKEN не задан. Проверьте .env", file=sys.stderr)
        sys.exit(1)

    chat_id = args.chat_id or get_chat_id()
    if not chat_id:
        print("Ошибка: chat_id не задан (--chat-id или TELEGRAM_CHAT_ID в .env)", file=sys.stderr)
        sys.exit(1)

    try:
        handler = TextHandler()
        text = handler.read(args.file)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {args.file}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Ошибка чтения файла: {e}", file=sys.stderr)
        sys.exit(1)

    chunks = handler.split_for_telegram(text)
    if not chunks:
        print("Файл пуст.", file=sys.stderr)
        sys.exit(0)

    client = TelegramClient(token)
    results = client.send_messages(chat_id, chunks)

    if all(ok for ok, _ in results):
        print(f"Отправлено {len(chunks)} сообщений в чат {chat_id}.")
    else:
        for i, (ok, err) in enumerate(results):
            if not ok and err:
                print(f"Ошибка Telegram API: {err}", file=sys.stderr)
                break
        failed = sum(1 for ok, _ in results if not ok)
        print(f"Не удалось отправить {failed} из {len(chunks)} сообщений.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
