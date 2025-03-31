# EXO BOT — CLEAN BUILD WITH CHAT ID DEBUGGING

from datetime import datetime, timedelta, timezone
from skyfield.api import load
import requests
import math
from collections import Counter, deque
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

BOT_TOKEN = "7753497642:AAEX3s9PTv_9oR24-Bz5K87l6FiPwVK0ALo"
CHAT_ID = "6732832197" 

planets = load('de430t.bsp')
ts = load.timescale()

# === BASIC FORECAST FUNCTION (PLACEHOLDER) ===
def generate_forecast():
    return "📡 Forecast system online."

# === TELEGRAM HANDLERS ===
async def startup(app):
    await app.bot.send_message(chat_id=CHAT_ID, text=generate_forecast())

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"👁 Chat ID Detected: {update.effective_chat.id}")
    await update.message.reply_text("📡 Chat ID received. Check your terminal.")

# === BUILD APP ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.post_init = startup
print("🚀 Exo is online.")

# === SCHEDULER ===
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Runs daily at 09:00 UTC — change as needed
    scheduler.add_job(lambda: app.bot.send_message(chat_id=CHAT_ID, text=generate_forecast()),
                      CronTrigger(hour=9, minute=0))
    scheduler.start()


start_scheduler()


# Replace polling with webhook setup
async def main():
    await app.bot.set_webhook(url="https://<https://exo-bot>.onrender.com")  # 👈 update this URL
    await app.initialize()
    await app.start()
    print("🚀 Exo is online with webhook.")
    await app.updater.start_polling()  # not required but can be used for debugging

import asyncio
asyncio.run(main())
