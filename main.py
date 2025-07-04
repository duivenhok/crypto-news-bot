import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = '7524161491:AAH4_dS3ZodefK6Vtn7ZOaOYRieaVzardKQ'
CHAT_ID = 7831457460
NEWS_API_KEY = 'ce322ee2bb1b452bb47db41d8973407d'

# Logging voor debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nieuws ophalen
def get_crypto_news():
    url = f'https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API_KEY}&language=en'
    response = requests.get(url)
    articles = response.json().get('articles', [])[:3]  # Laatste 3 artikelen
    return articles

# /ping commando
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Pong! De bot reageert.")

# /forcecheck commando
async def forcecheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = get_crypto_news()
    if not articles:
        await update.message.reply_text("⚠️ Geen nieuws gevonden.")
        return

    for art in articles:
        msg = f"📰 {art['title']}\n🔗 {art['url']}\n📡 Bron: {art['source']['name']}"
        await update.message.reply_text(msg)

# Opstartmelding
async def startup_notify(app):
    await app.bot.send_message(chat_id=CHAT_ID, text="🚀 Bot draait en luistert naar nieuws!")

# Hoofd-app
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("forcecheck", forcecheck))

    app.post_init = startup_notify

    app.run_polling()

if __name__ == "__main__":
    main()
