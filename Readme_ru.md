# Telegram Planka Bot 2.0

## Описание

Этот Telegram-бот предназначен для получения информации о карточках в [Planka](https://github.com/plankanban/planka) **версии 2.0** на конкретную дату. Инструмент позволяет легко контролировать назначенные дела и не пропускать ничего важного, даже если задач и досок очень много. Просто нажмите кнопку в боте, чтобы мгновенно получить актуальный список задач на сегодня/на завтра/на неделю. Даже если у вас 10 проектов и 100 досок.

Если вы используете Planka **версии 1.x**, смотрите [Bot_checker_date_planka](https://github.com/john-gear/bot_checker_date_planka).

### Возможности:

- **Задачи на сегодня** — бот отправит список задач, назначенных на сегодня, а также список просроченных задач (например, за вчера или прошлую неделю). Удобно для ежедневного планирования.
- **Задачи на завтра** — покажет список задач, назначенных на следующий день. Полезно при планировании встреч и задач на завтра.
- **Задачи на неделю** — отправит все задачи на ближайшие 7 дней. Это поможет избежать авралов и лучше распределить нагрузку.
- **Задачи на дату** — позволяет узнать, какие задачи назначены на конкретную дату. Например, если у вас день рождения 26 апреля, можно заранее посмотреть, какие дела запланированы.

## Демонстрация
![Демонстрация работы](https://github.com/garpastyls/bot_checker_date_planka/blob/main/work_demonstration.gif)

## Состав проекта

- `config.py` — содержит авторизационные данные Planka, список досок для мониторинга, ID пользователей с доступом к боту.
- `checker_date_planka.py` — точка входа в программу (запуск через `python checker_date_planka.py`).

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/garpastyls/bot_checker_date_planka.git
cd Trello_downloader
```

### 2. Создание виртуального окружения

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка `config.py`

- Добавьте ключи API Planka.
- Укажите ID досок Planka для мониторинга.
- Вставьте Telegram-токен и ID пользователей, которым разрешен доступ к боту.

### 5. Запуск скрипта для теста

```bash
python checker_date_planka.py
```

### 6. Запуск с PM2 (для постоянной работы в фоне)

PM2 — это менеджер процессов, который помогает запускать и перезапускать бота при сбоях.

#### Установка PM2

```bash
npm install -g pm2
```

#### Запуск бота с PM2

```bash
pm2 start checker_date_planka.py --name planka-bot --interpreter python3.11
pm2 save
pm2 startup
```

#### Управление процессом

- Проверить статус:
  ```bash
  pm2 status
  ```
- Перезапустить бота:
  ```bash
  pm2 restart planka-bot
  ```
- Остановить бота:
  ```bash
  pm2 stop planka-bot
  ```
- Удалить процесс из PM2:
  ```bash
  pm2 delete planka-bot
  ```

## Получение API Planka

1. Заполните `PLANKA_URL` ссылкой на ваш сервер Planka.
2. Укажите `USERNAME` и `PASSWORD` для входа в Planka.
3. Создайте Telegram-бота через `@BotFather` и получите `TELEGRAM_TOKEN`.
4. Узнайте свой Telegram ID с помощью `@getmyid_bot` и добавьте в `ALLOWED_USERS`.
5. Найдите ID досок Planka (например, взяв из ссылки `https://planka.com/boards/0123456789` значение после `/boards/`) и укажите в `BOARD_IDS`.
6. Укажите ваш часовой пояс в `TIMEZONE`.

### Пример `config.py`

```python
# Данные для авторизации в Planka
PLANKA_URL = "https://planka.com/api"  # Не убирайте /api в конце
USERNAME = "admin"
PASSWORD = "admin"

# Настройки Telegram
TELEGRAM_TOKEN = "your_telegram_api_token"
ALLOWED_USERS = [123456789]  # ID пользователей с доступом к боту

# ID досок для мониторинга
BOARD_IDS = [
    "0123456789",  # Доска #1 в Planka
    "987654321",  # Доска #2 в Planka
]

# Часовой пояс
import pytz
TIMEZONE = pytz.timezone("Europe/Moscow")
```

## Зависимости

Все необходимые библиотеки указаны в `requirements.txt`:

```
requests
aiogram
pytz
datetime
asyncio
```

Установите их командой:

```bash
pip install -r requirements.txt
```

## Особенности работы

- Все действия бота логируются в файле `bot.log`. Лог очищается еженедельно.
- Комментарии к задачам ограничены 50 символами. При необходимости можно увеличить этот лимит, изменив строку:
  ```python
  {comments[0]["text"][:50]}  # Ограничение в 50 символов
  ```

## Лицензия

Проект распространяется под лицензией MIT.

## Обратная связь

Если у вас есть вопросы или проблемы — создавайте issue в репозитории!

## 💡Если Вы сочли мой проект полезным, Вы можете поддержать меня финансово — даже небольшое пожертвование имеет значение
- **Crypto donation: USDT (TRC20):** `TCECqH8ZxXGCQuWZeto1nV9nawbeeV4fG8`
- **Crypto donation: Bitcoin (BTC):** `bc1q3lvprzayxd3qulk0epk5dh58zx36mfev76wj30`
- **Crypto donation: Ethereum (ETH):** `0x80DbC00Fd91bAb3D4FE6E6441Dae0719e6bF5c9e`
- **International card (Visa/Mastercard):**  
[https://www.donationalerts.com/r/johngear](https://www.donationalerts.com/r/johngear)
