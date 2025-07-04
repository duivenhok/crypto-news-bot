
import os
import threading
import requests
import time
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

def send_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

def start(update, context):
    send_message("✅ Bot is gestart en klaar! Gebruik /ping of /forcecheck.")

def ping(update, context):
    update.message.reply_text("✅ Pong! De bot reageert.")

def forcecheck(update, context):
    send_message("🔎 Haal nu nieuws op...")
    fetch_and_send_news()

def fetch_and_send_news():
    url = ("https://newsapi.org/v2/everything?"
           "q=crypto&language=en&sortBy=publishedAt&pageSize=3&apiKey=" + NEWSAPI_KEY)
    resp = requests.get(url).json()
    articles = resp.get('articles', [])
    if not articles:
        send_message("⚠️ Geen nieuws gevonden")
    else:
        for art in articles:
            message = f"📰 {art['title']}\n🔗 {art['url']}\n🕒 {art['publishedAt']}\n📡 Bron: {art['source']['name']}"
send_message(message)
🔗 {art['url']}")

def periodic_news():
    while True:
        fetch_and_send_news()
        time.sleep(3600)  # elk uur

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("forcecheck", forcecheck))
    updater.start_polling()
    send_message("🚀 Bot draait 24/7!")
    t = threading.Thread(target=periodic_news, daemon=True)
    t.start()
    updater.idle()

if __name__ == "__main__":
    main()
