import pytz

# Data for authorisation in Planka
PLANKA_URL = "https://planka.com/api" # Leave /api at the end of the domain 
USERNAME = "admin"
PASSWORD = "admin"
TELEGRAM_TOKEN = "your_telegram_api_token" # Telegram bot token
ALLOWED_USERS = [288583210] # Allowed bot users. You can get your user-id in the Telegram bot @getmyid_bot
BOARD_IDS = [
    "0123456789", # Board #1 at Planka
    "0123456789", # Board #2 at Planka
    # List of board IDs in Planka (available in the link https://planka.com/boards/0123456789 , take the numbers after /boards/)
]
TIMEZONE = pytz.timezone("Europe/Moscow") # set your time zone to display the comment time correctly
