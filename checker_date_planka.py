import requests
import logging
import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
import re
import os
from config import PLANKA_URL, USERNAME, PASSWORD, TELEGRAM_TOKEN, ALLOWED_USERS, BOARD_IDS, TIMEZONE

# Function: obtaining Bearer token in Planka
def get_token():
    url = f"{PLANKA_URL}/access-tokens"
    payload = {"emailOrUsername": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        for key in ["token", "item", "id"]:
            if key in data:
                return data[key]
    except requests.RequestException:
        return None
    return None

# Function: clears the comment from unnecessary spaces and line breaks
def clean_comment(text):
    return re.sub(r"\s+", " ", text).strip()

# Function: retrieves the last comment in the Planka card
def get_last_comment(token, card_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{PLANKA_URL}/cards/{card_id}/comments"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "items" not in data or not data["items"]:
            return ""

        comments = [
            {
                "text": clean_comment(c["text"]),
                "createdAt": datetime.datetime.fromisoformat(c["createdAt"].replace("Z", ""))
            }
            for c in data["items"]
        ]

        if comments:
            comments.sort(key=lambda x: x["createdAt"], reverse=True)
            return comments[0]["text"][:50]

        return ""
    except Exception:
        return ""

# Function: receiving cards with their deadlines
def get_due_cards(token, start_date, end_date):
    headers = {"Authorization": f"Bearer {token}"}
    result = {}

    projects_url = f"{PLANKA_URL}/projects"
    projects_response = requests.get(projects_url, headers=headers).json()
    projects = projects_response["items"]

    for project in projects:
        project_name = project["name"]
        project_id = project["id"]

        boards_url = f"{PLANKA_URL}/projects/{project_id}"
        boards_response = requests.get(boards_url, headers=headers).json()
        boards = boards_response["included"].get("boards", [])

        filtered_boards = [b for b in boards if b["id"] in BOARD_IDS]

        for board in filtered_boards:
            board_name = board["name"]
            board_id = board["id"]

            board_url = f"{PLANKA_URL}/boards/{board_id}"
            board_response = requests.get(board_url, headers=headers).json()

            included = board_response["included"]
            lists = included.get("lists", [])
            list_types = {lst["id"]: lst.get("type", "") for lst in lists}
            valid_list_ids = set(list_types.keys())

            cards = included.get("cards", [])

            for card in cards:
                list_id = card.get("listId")
                if not list_id or list_id not in valid_list_ids:
                    continue
                if list_types[list_id].lower() == "closed":
                    continue

                due_date = card.get("dueDate")
                completed = card.get("isDueDateCompleted", False)

                if due_date and not completed:
                    due_date_obj = datetime.datetime.fromisoformat(due_date.replace("Z", "")).replace(
                        tzinfo=datetime.timezone.utc).astimezone(TIMEZONE)
                    due_date_date = due_date_obj.date()

                    if start_date <= due_date_date <= end_date:
                        short_name = (card["name"][:30] + "...") if len(card["name"]) > 30 else card["name"]
                        comment = get_last_comment(token, card["id"])

                        if project_name not in result:
                            result[project_name] = {}
                        if board_name not in result[project_name]:
                            result[project_name][board_name] = []

                        result[project_name][board_name].append(
                            (short_name, due_date_obj.strftime("%d-%m-%Y %H:%M"), comment)
                        )

    return result

# Authorisation in the Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Setting up buttons in the Telegram bot
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗓 Tasks for today")],
        [KeyboardButton(text="🗓 Tomorrow's tasks")],
        [KeyboardButton(text="🗓 Tasks for the week")],
        [KeyboardButton(text="🗓 Date tasks")]
    ],
    resize_keyboard=True
)

# Handler for the /start command
@dp.message(Command("start"))
async def start(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS: # ALLOWED_USERS check
        return await message.reply("You're not allowed access to the bot") 
    await message.reply("Hi. Choose an action by clicking on the button below to get information from your Planka", reply_markup=keyboard)

# Button handler
@dp.message(F.text.in_(["🗓 Tasks for today", "🗓 Tomorrow's tasks", "🗓 Tasks for the week"]))
async def send_tasks(message: types.Message):
    today = datetime.datetime.now(TIMEZONE).date()
    tomorrow = today + datetime.timedelta(days=1)

    if message.text == "🗓 Tasks for today":
        start_date = datetime.date.min
        end_date = today
    elif message.text == "🗓 Tomorrow's tasks":
        start_date = end_date = tomorrow
    elif message.text == "🗓 Tasks for the week":
        start_date = today
        end_date = today + datetime.timedelta(days=7)
    else:
        return await message.reply("Unrecognized command")

    token = get_token()
    tasks = get_due_cards(token, start_date, end_date)

    if not tasks:
        return await message.reply("There are no tasks for the selected period")

    response_text = ""
    for project, boards in tasks.items():
        response_text += f"\n----- Project: <b>{project}</b> -----\n"
        for board, cards in boards.items():
            response_text += f"\nBoard: <b>{board}</b>\n"
            for name, date, comment in cards:
                response_text += f"\n📄 Card: {name}(🕒 {date})\n"
                if comment:
                    response_text += f"<i>💬 Comment: {comment}</i>\n"
            response_text += "---\n"

    await message.reply(response_text.strip(), reply_markup=keyboard, parse_mode="HTML")

# Handler of the ‘Tasks on date’ button
@dp.message(F.text == "🗓 Date tasks")
async def ask_date(message: types.Message):
    await message.reply("Enter the date in DD-MM-YYYYY format (e.g. 10-06-2025)")

@dp.message(F.text.regexp(r"\d{2}-\d{2}-\d{4}"))
async def tasks_by_date(message: types.Message):
    try:
        target_date = datetime.datetime.strptime(message.text, "%d-%m-%Y").date()
    except ValueError:
        return await message.reply("Incorrect date format. Use DD-MM-YYYYY (be sure to use the '-' character)")

    token = get_token()
    tasks = get_due_cards(token, target_date, target_date)

    if not tasks:
        return await message.reply("Congratulations! There are no tasks for the selected period!")

    response_text = ""
    for project, boards in tasks.items():
        response_text += f"\n----- Project: <b>{project}</b> -----\n"
        for board, cards in boards.items():
            response_text += f"\nBoard: <b>{board}</b>\n"
            for name, date, comment in cards:
                response_text += f"\n📄 Card: {name}(🕒 {date})\n"
                if comment:
                    response_text += f"<i>Comment: {comment}</i>\n"
            response_text += "---\n"

    await message.reply(response_text.strip() or "Congratulations! There are no tasks for the selected period!", reply_markup=keyboard, parse_mode="HTML")

# Launching Telegram bot
async def main():
    while True:
        try:
            await dp.start_polling(bot, timeout=60)
        except Exception:
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())