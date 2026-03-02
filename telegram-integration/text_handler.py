"""Обработка текста из файла для отправки в Telegram."""

TELEGRAM_MAX_MESSAGE_LENGTH = 4096


class TextHandler:
    """Чтение и подготовка текста для отправки."""

    def __init__(self, max_length: int = TELEGRAM_MAX_MESSAGE_LENGTH):
        self.max_length = max_length

    def read(self, path: str) -> str:
        """Читает текст из файла. Кодировка UTF-8."""
        with open(path, encoding="utf-8") as f:
            return f.read()

    def split_for_telegram(self, text: str) -> list[str]:
        """
        Разбивает текст на части не длиннее max_length.
        Старается разрывать по переносам строк.
        """
        if len(text) <= self.max_length:
            return [text] if text else []

        chunks: list[str] = []
        remaining = text

        while remaining:
            if len(remaining) <= self.max_length:
                chunks.append(remaining)
                break

            segment = remaining[: self.max_length]
            last_newline = segment.rfind("\n")

            if last_newline > 0:
                cut = last_newline + 1
            else:
                cut = self.max_length

            chunks.append(remaining[:cut])
            remaining = remaining[cut:] if cut < len(remaining) else ""

        return chunks
