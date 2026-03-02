#!/usr/bin/env python3
"""
Проверка email-доменов по MX-записям.
Принимает список email-адресов (аргументы или файл) и выводит статус для каждого.
"""

import argparse
import re
import sys

import dns.exception
import dns.resolver


DNS_TIMEOUT = 5
DNS_LIFETIME = 10


def extract_domain(email: str) -> str | None:
    """Извлекает домен из email-адреса."""
    if not email or not isinstance(email, str):
        return None
    pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
    match = re.match(pattern, email.strip())
    return match.group(1) if match else None


def check_mx(domain: str) -> tuple[str, bool]:
    """
    Проверяет MX-записи домена.
    Возвращает (статус, успех): успех=False для временных ошибок (сеть, таймаут).
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_LIFETIME

    try:
        mx_records = resolver.resolve(domain, 'MX')
        if mx_records:
            return 'домен валиден', True
        return 'MX-записи отсутствуют или некорректны', True
    except dns.resolver.NXDOMAIN:
        return 'домен отсутствует', True
    except dns.resolver.NoAnswer:
        return 'MX-записи отсутствуют или некорректны', True
    except dns.resolver.NoNameservers:
        return 'домен отсутствует', True
    except dns.exception.Timeout:
        return 'ошибка: таймаут DNS-запроса', False
    except (OSError, ConnectionError) as e:
        return f'ошибка: сетевая ошибка ({e.__class__.__name__})', False
    except dns.exception.DNSException as e:
        return f'ошибка DNS: {e}', False


def load_emails_from_file(path: str) -> list[str]:
    """Читает email-адреса из файла (по одному на строку)."""
    try:
        with open(path, encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except OSError as e:
        print(f'Ошибка чтения файла {path}: {e}', file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Проверка email-доменов по MX-записям.'
    )
    parser.add_argument(
        '-f', '--file',
        metavar='FILE',
        help='файл со списком email (по одному на строку)'
    )
    parser.add_argument(
        'emails',
        nargs='*',
        metavar='email',
        help='email-адреса для проверки'
    )
    args = parser.parse_args()

    emails: list[str] = []
    if args.file:
        emails = load_emails_from_file(args.file)
    if args.emails:
        emails.extend(email.strip() for email in args.emails if email.strip())

    if not emails:
        parser.print_help()
        print('\nОшибка: не указаны email-адреса (используйте -f FILE или укажите адреса).')
        sys.exit(1)

    exit_code = 0
    for email in emails:
        try:
            domain = extract_domain(email)
            if not domain:
                print(f'{email}: некорректный формат email')
                continue
            status, ok = check_mx(domain)
            print(f'{email}: {status}')
            if not ok:
                exit_code = 1
        except KeyboardInterrupt:
            print('\nПрервано пользователем.', file=sys.stderr)
            sys.exit(130)
        except Exception as e:
            print(f'{email}: неожиданная ошибка ({e.__class__.__name__}: {e})', file=sys.stderr)
            exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
