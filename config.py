import os

from dotenv import load_dotenv

load_dotenv()

# Telegram bot token
TOKEN = os.environ.get('TOKEN')

APOD_API_KEY = os.environ.get("APOD_API_KEY", "DEMO_KEY")
APOD_API_URL = f"https://api.nasa.gov/planetary/apod?api_key={APOD_API_KEY}"
APOD_URL = "https://apod.nasa.gov/apod/"
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

START_MESSAGE = "Hola!"
HELP_MESSAGE = "HELP"
