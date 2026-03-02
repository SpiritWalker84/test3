"""Клиент для отправки сообщений через Telegram Bot API."""

import requests


class TelegramClient:
    """Обёртка над Telegram Bot API для отправки сообщений."""

    API_BASE = "https://api.telegram.org/bot{token}"

    def __init__(self, token: str):
        self.token = token
        self._base_url = self.API_BASE.format(token=token)

    def send_message(self, chat_id: str, text: str) -> tuple[bool, str | None]:
        """
        Отправляет текстовое сообщение в чат.
        Возвращает (успех, текст_ошибки).
        """
        url = f"{self._base_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()
        except requests.RequestException as e:
            return False, str(e)
        if not data.get("ok", False):
            desc = data.get("description", "Unknown error")
            return False, desc
        return True, None

    def send_messages(self, chat_id: str, texts: list[str]) -> list[tuple[bool, str | None]]:
        """Отправляет список сообщений. Возвращает [(успех, ошибка), ...]."""
        return [self.send_message(chat_id, t) for t in texts]
