# app/telegram_bot/handlers.py
from .bot import bot
from .buttons import main_menu, start_button, auth_menu
from app.database import SessionLocal
from app import crud, schemas
from telebot import types

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в Finance Bot! Пожалуйста, зарегистрируйтесь или войдите, чтобы начать управлять своими финансами.", reply_markup=start_button())

# Обработчик кнопки "Старт"
@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_menu())


# Обработчик кнопки "Регистрация"
@bot.message_handler(func=lambda message: message.text == "Регистрация")
def handle_registration(message):
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, process_registration_name)

def process_registration_name(message):
    name = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите вашу электронную почту:")
    bot.register_next_step_handler(message, process_registration_email, name)

def process_registration_email(message, name):
    email = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите ваш пароль:")
    bot.register_next_step_handler(message, process_registration_password, name, email)

def process_registration_password(message, name, email):
    password = message.text
    chat_id = message.chat.id
    db = SessionLocal()
    existing_user = crud.get_user_by_email(db, email)
    if existing_user:
        bot.send_message(chat_id, "Этот email уже зарегистрирован. Попробуйте снова.")
        db.close()
        return
    user_data = {'name': name, 'email': email, 'password': password}
    crud.create_user(db, schemas.UserCreate(**user_data))
    db.close()
    bot.send_message(chat_id, "Регистрация завершена. Теперь вы можете войти.", reply_markup=auth_menu())

# Обработчик кнопки "Вход"
@bot.message_handler(func=lambda message: message.text == "Вход")
def handle_login(message):
    bot.send_message(message.chat.id, "Введите вашу электронную почту:")
    bot.register_next_step_handler(message, process_login_email)

def process_login_email(message):
    email = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите ваш пароль:")
    bot.register_next_step_handler(message, process_login_password, email)

def process_login_password(message, email):
    password = message.text
    chat_id = message.chat.id
    db = SessionLocal()
    user = crud.get_user_by_email(db, email)
    if user and crud.pwd_context.verify(password, user.hashed_password):
        bot.send_message(chat_id, f"Вход выполнен. Добро пожаловать, {user.name}!", reply_markup=main_menu())
    else:
        bot.send_message(chat_id, "Неправильная электронная почта или пароль. Попробуйте снова.")
    db.close()

# Обработчик кнопки "Добавить доход"
@bot.message_handler(func=lambda message: message.text == "Добавить доход")
def handle_add_income(message):
    bot.send_message(message.chat.id, "Введите сумму дохода:")

# Обработчик кнопки "Добавить расход"
@bot.message_handler(func=lambda message: message.text == "Добавить расход")
def handle_add_expense(message):
    bot.send_message(message.chat.id, "Введите сумму расхода:")

# Обработчик кнопки "Просмотр истории"
@bot.message_handler(func=lambda message: message.text == "Просмотр истории")
def handle_view_history(message):
    bot.send_message(message.chat.id, "Вот ваша история транзакций:")

# Обработчик кнопки "Сводка"
@bot.message_handler(func=lambda message: message.text == "Сводка")
def handle_summary(message):
    bot.send_message(message.chat.id, "Вот ваша финансовая сводка:")
