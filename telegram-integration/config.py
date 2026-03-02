"""Загрузка конфигурации из переменных окружения."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Загрузить .env из директории скрипта
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)


def get_bot_token() -> str | None:
    """Возвращает токен бота из TELEGRAM_BOT_TOKEN."""
    return os.getenv("TELEGRAM_BOT_TOKEN")


def get_chat_id() -> str | None:
    """Возвращает chat_id из TELEGRAM_CHAT_ID."""
    return os.getenv("TELEGRAM_CHAT_ID")
