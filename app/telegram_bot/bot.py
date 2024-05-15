# app/telegram_bot/bot.py
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

from . import handlers

def run():
    bot.polling()
