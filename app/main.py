# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, transactions
from app.telegram_bot.bot import run as run_bot
import threading

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])


bot_thread = threading.Thread(target=run_bot)
bot_thread.start()
