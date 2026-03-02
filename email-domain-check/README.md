# Email Domain Checker

Проверка email-адресов по MX-записям DNS. Скрипт принимает список email, извлекает домены и проверяет наличие MX-записей.

## Требования

- Python 3.10+
- Windows (пути указаны для PowerShell/cmd)

## Структура

```
email_domain_check.py   # основной скрипт
requirements.txt       # зависимости (dnspython)
emails.txt             # пример списка для проверки
```

## Установка

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

При ошибке выполнения скриптов в PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Запуск

```powershell
.\venv\Scripts\python email_domain_check.py [OPTIONS] [email ...]
```

**Аргументы:**

| Параметр | Описание |
|----------|----------|
| `-f`, `--file FILE` | Файл со списком email (по одному на строку) |
| `email` | Email-адреса для проверки (позиционные аргументы) |

Флаг `-f` и позиционные аргументы можно комбинировать.

**Примеры:**

```powershell
.\venv\Scripts\python email_domain_check.py user@example.com admin@test.org
.\venv\Scripts\python email_domain_check.py -f emails.txt
.\venv\Scripts\python email_domain_check.py -f emails.txt extra@domain.com
```

## Выходные статусы

| Статус | Условие |
|--------|---------|
| `домен валиден` | MX-записи найдены |
| `домен отсутствует` | NXDOMAIN, нет NS |
| `MX-записи отсутствуют или некорректны` | Домен резолвится, MX-записей нет |

Дополнительно: `некорректный формат email` — невалидный формат адреса; сообщения об ошибках при таймаутах и сетевых сбоях.

## Код возврата

- `0` — успешное выполнение
- `1` — ошибка (некорректный ввод, таймаут, сетевая ошибка, неожиданное исключение)
