import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TELEGRAM_TOKEN = "7524161491:AAH4_dS3ZodefK6Vtn7ZOaOYRieaVzardKQ"
CHAT_ID = 7831457460
NEWS_API_KEY = "ce322ee2bb1b452bb47db41d8973407d"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_crypto_news():
    url = f"https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:3]
    return articles


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Pong! De bot reageert.")


async def forcecheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = get_crypto_news()
    if not articles:
        await update.message.reply_text("⚠️ Geen nieuws gevonden.")
        return

    for art in articles:
        msg = f"📰 {art['title']}\n🔗 {art['url']}\n📡 Bron: {art['source']['name']}"
        await update.message.reply_text(msg)


async def startup_notify(app):
    await app.bot.send_message(chat_id=CHAT_ID, text="🚀 Bot draait en luistert naar nieuws!")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("forcecheck", forcecheck))

    app.post_init = startup_notify

    app.run_polling()


if __name__ == "__main__":
    main()
