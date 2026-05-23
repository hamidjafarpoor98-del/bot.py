import os
import telebot
from telebot import types

# گرفتن توکن از Render
TOKEN = os.getenv("TOKEN")

# چک کردن اینکه توکن وجود دارد
if not TOKEN:
    raise ValueError("TOKEN تنظیم نشده!")

ADMIN_ID = 432039844

bot = telebot.TeleBot(TOKEN)

# --------------------
# شروع ربات
# --------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buy_btn = types.KeyboardButton("خرید ۱ گیگ ۳۰ روزه")
    markup.add(buy_btn)

    bot.send_message(
        message.chat.id,
        "یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup
    )

# --------------------
# دکمه خرید
# --------------------
@bot.message_handler(func=lambda message: message.text == "خرید ۱ گیگ ۳۰ روزه")
def buy(message):
    text = """برای خرید ۱ گیگ مبلغ 480 تومان را به شماره کارت زیر واریز کنید:

5892101261141630

بعد از پرداخت، رسید را ارسال کنید."""
    
    bot.send_message(message.chat.id, text)

# --------------------
# دریافت همه پیام‌ها
# --------------------
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document'])
def all_messages(message):

    username = message.from_user.username
    if username:
        username = "@" + username
    else:
        username = "ندارد"

    user_info = f"""پیام جدید از کاربر:

آیدی: {username}
نام: {message.from_user.first_name}
آیدی عددی: {message.from_user.id}
"""

    bot.send_message(ADMIN_ID, user_info)

    # فوروارد پیام برای ادمین
    bot.forward_message(
        ADMIN_ID,
        message.chat.id,
        message.message_id
    )

    bot.reply_to(
        message,
        "رسید شما ارسال شد، بعد از تایید اطلاع داده می‌شود."
    )

print("Bot Started...")
bot.infinity_polling()
