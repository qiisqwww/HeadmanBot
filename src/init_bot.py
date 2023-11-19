from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from src.config import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)