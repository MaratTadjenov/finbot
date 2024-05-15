# app/telegram_bot/buttons.py
from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить доход")
    btn2 = types.KeyboardButton("Добавить расход")
    btn3 = types.KeyboardButton("Просмотр истории")
    btn4 = types.KeyboardButton("Сводка")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def start_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Старт")
    markup.add(btn1)
    return markup


def auth_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Регистрация")
    btn2 = types.KeyboardButton("Вход")
    markup.add(btn1, btn2)
    return markup
