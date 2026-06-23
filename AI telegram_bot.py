import telebot
from groq import Groq
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8398009719:AAFSp_hF9f9M0_NRRx9tJZ2-lFc9Rn5q8F8")
GROQ_KEY = os.environ.get("GROQ_KEY", "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")

client = Groq(api_key=GROQ_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def salom(message):
    bot.reply_to(message,
        "Salom! 👋 Men AI botman.\n"
        "Menga istalgan savol bering — javob beraman!"
    )

@bot.message_handler(func=lambda m: True)
def ai_javob(message):
    savol = message.text

    if savol.startswith('/'):
        return

    yuklash = bot.reply_to(message, "⏳ Javob tayyorlanmoqda...")

    try:
        javob = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Sen foydali AI yordamchisan. Har doim o'zbek tilida javob ber."
                },
                {
                    "role": "user",
                    "content": savol
                }
            ]
        )
        javob_matni = javob.choices[0].message.content

    except Exception as e:
        javob_matni = f"Xatolik: {str(e)}"

    bot.delete_message(message.chat.id, yuklash.message_id)
    bot.send_message(message.chat.id, javob_matni)

print("Bot ishlayapti... 🚀")
bot.polling()