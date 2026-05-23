import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not TOKEN:
    raise ValueError("TOKEN تنظیم نشده!")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL تنظیم نشده!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --------------------
# صفحه تست
# --------------------
@app.route("/", methods=["GET"])
def home():
    return "Bot is running 🚀"

# --------------------
# Webhook endpoint
# --------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    return "Invalid request", 403

# --------------------
# /start
# --------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("خرید ۱ گیگ ۳۰ روزه"))

    bot.send_message(
        message.chat.id,
        "یکی از گزینه‌ها را انتخاب کنید 👇",
        reply_markup=markup
    )

# --------------------
# خرید
# --------------------
@bot.message_handler(func=lambda m: m.text == "خرید ۱ گیگ ۳۰ روزه")
def buy(message):
    bot.send_message(
        message.chat.id,
        "💰 مبلغ 480 تومان\n\n💳 5892101261141630\n\nرسید ارسال کنید 📩"
    )

# --------------------
# پیام‌ها (فوروارد به ادمین)
# --------------------
@bot.message_handler(func=lambda m: True, content_types=['text', 'photo', 'document'])
def all_messages(message):

    username = message.from_user.username
    username = f"@{username}" if username else "ندارد"

    text = f"""
📩 پیام جدید

👤 {username}
🆔 {message.from_user.id}
"""

    if ADMIN_ID:
        bot.send_message(ADMIN_ID, text)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

# --------------------
# ست کردن webhook (مهم)
# --------------------
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

print("Bot is running with webhook 🚀")
