# Telegram Planka Bot

## Description

This Telegram bot is designed to fetch information about cards in **Planka version 2.0** for a specific date. It helps you easily stay on top of your assigned tasks and never miss anything important — even if you have many boards and projects. Just press a button in the bot to instantly receive an up-to-date list of tasks for today, tomorrow, or the upcoming week — even if you're managing 10 projects and 100 boards.

If you're using **Planka version 1.x**, check out the [legacy branch](https://github.com/garpastyls/bot_checker_date_planka/tree/legacy).

### Features:

- **Tasks for today** — The bot will send a list of tasks scheduled for today, along with overdue tasks (e.g., from yesterday or last week). This is useful for daily planning.
- **Tasks for tomorrow** — View tasks scheduled for the next day. Ideal for planning meetings and workload in advance.
- **Tasks for the week** — Get all tasks for the next seven days to avoid last-minute rushes and better distribute workload.
- **Tasks for a specific date** — Check tasks assigned to a particular date. For example, if your birthday is on April 26, you can see in advance how your day is structured to plan accordingly.

## Demonstration
![Work Demonstration](https://github.com/garpastyls/bot_checker_date_planka/blob/main/work_demonstration.gif)

## Project Structure

- `config.py` — Contains Planka authentication data, a list of monitored boards, and IDs of users who can access the bot.
- `checker_date_planka.py` — The main entry point of the program (run using `python checker_date_planka.py`).

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/garpastyls/bot_checker_date_planka.git
cd Trello_downloader
```

### 2. Create a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `config.py`

- Add Planka API keys.
- Specify the Planka board IDs to monitor.
- Insert the Telegram bot token and allowed user IDs.

### 5. Run the script for testing

```bash
python checker_date_planka.py
```

### 6. Run the bot with PM2 (for continuous operation)

PM2 is a process manager that ensures the bot runs continuously and restarts in case of failures.

#### Install PM2

```bash
npm install -g pm2
```

#### Start the bot using PM2

```bash
pm2 start checker_date_planka.py --name planka-bot --interpreter python3.11
pm2 save
pm2 startup
```

#### Manage the process

- Check status:
  ```bash
  pm2 status
  ```
- Restart the bot:
  ```bash
  pm2 restart planka-bot
  ```
- Stop the bot:
  ```bash
  pm2 stop planka-bot
  ```
- Remove the process from PM2:
  ```bash
  pm2 delete planka-bot
  ```

## Obtaining Planka API Credentials

1. Set `PLANKA_URL` with the URL of your Planka instance.
2. Enter your `USERNAME` and `PASSWORD` for Planka authentication.
3. Create a Telegram bot using `@BotFather` and obtain your `TELEGRAM_TOKEN`.
4. Get your Telegram user ID using `@getmyid_bot` and add it to `ALLOWED_USERS`.
5. Retrieve Planka board IDs from the URL (e.g., for `https://planka.com/boards/0123456789`, take the numbers after `/boards/`) and list them in `BOARD_IDS`.
6. Set your time zone in `TIMEZONE`.

### Example `config.py`

```python
# Authentication data for Planka
PLANKA_URL = "https://planka.com/api"  # Keep /api at the end
USERNAME = "admin"
PASSWORD = "admin"

# Telegram settings
TELEGRAM_TOKEN = "your_telegram_api_token"
ALLOWED_USERS = [123456789]  # Allowed bot users

# Monitored board IDs
BOARD_IDS = [
    "0123456789",  # Board #1 in Planka
    "987654321",  # Board #2 in Planka
]

# Time zone
import pytz
TIMEZONE = pytz.timezone("Europe/Moscow")
```

## Dependencies

All required libraries are listed in `requirements.txt`:

```
requests
aiogram
pytz
datetime
asyncio
```

Install them with:

```bash
pip install -r requirements.txt
```

## Bot Functionality

- All bot actions are logged in `bot.log`, which is cleared weekly.
- Task comments are limited to 50 characters. To increase the limit, modify the following line:
  ```python
  {comments[0]["text"][:50]}  # Limit to 50 characters
  ```

## License

This project is distributed under the MIT License.

## Feedback

If you have any questions or issues, feel free to create an issue in the repository!
