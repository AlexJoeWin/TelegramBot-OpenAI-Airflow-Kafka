import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_TOKEN")
TELEGRAM_KEY = os.getenv("BOT_TOKEN")