# Мини-интеграция с Telegram

Скрипт отправляет текст из .txt файла в приватный Telegram-чат через бота.

## Требования

- Python 3.10+
- Бот, созданный через [@BotFather](https://t.me/BotFather)
- Бот добавлен в чат, chat_id известен

## Установка

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Конфигурация

Скопируйте `.env.example` в `.env` и заполните:

```powershell
copy .env.example .env
```

| Переменная | Описание |
|------------|----------|
| `TELEGRAM_BOT_TOKEN` | Токен бота от BotFather |
| `TELEGRAM_CHAT_ID` | ID чата (число или @username) |

## Запуск

```powershell
.\venv\Scripts\python main.py <путь_к_файлу.txt>
.\venv\Scripts\python main.py message.txt --chat-id 123456789
```

**Аргументы:**

| Параметр | Описание |
|----------|----------|
| `file` | Путь к .txt файлу |
| `--chat-id` | Переопределяет TELEGRAM_CHAT_ID из .env |

Текст длиннее 4096 символов разбивается на несколько сообщений (разрыв по строкам).

## Результат

![Скриншот сообщения в Telegram](example.png)
