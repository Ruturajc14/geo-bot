import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================================
# 🔑 YOUR TELEGRAM BOT TOKEN
# ================================
BOT_TOKEN = "8547149588:AAE2XmSZsjHgX6fKzrXxQDwobWV9UCzValM"

# ================================
# 🌐 FLASK WEB SERVER (RENDER)
# ================================
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()

# ================================
# 🤖 TELEGRAM COMMAND
# ================================
async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text("✅ Bot is working!\nExample:\n/geo Will China invade Taiwan?")
        return

    await update.message.reply_text(f"🌍 Geopolitical analysis coming soon...\nQuestion: {question}")

# ================================
# 🚀 START TELEGRAM BOT
# ================================
async def main():
    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("geo", geo))

    print("🤖 Telegram bot started...")

    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)  # IMPORTANT
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
