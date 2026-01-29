import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# ================================
# 🔑 YOUR TELEGRAM BOT TOKEN
# ================================
BOT_TOKEN = "8547149588:AAE2XmSZsjHgX6fKzrXxQDwobWV9UCzValM"

# ================================
# 🌍 YOUR RENDER URL (IMPORTANT)
# ================================
WEBHOOK_URL = "https://geo-bot-k0f4.onrender.com"

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

# ================================
# 🤖 TELEGRAM COMMAND
# ================================
async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)
    
    if not question:
        await update.message.reply_text("✅ Bot is working!\nExample:\n/geo Will China invade Taiwan?")
        return
    
    await update.message.reply_text(f"🌍 Geopolitical analysis:\n{question}")

# ================================
# TELEGRAM APP
# ================================
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("geo", geo))

# ================================
# WEBHOOK ROUTE
# ================================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

# ================================
# ROOT ROUTE (HEALTH CHECK)
# ================================
@app.route("/")
def home():
    return "🤖 Geopolitical Bot is running with webhook!"

# ================================
# SET WEBHOOK
# ================================
def set_webhook():
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    print("✅ Webhook set!")

set_webhook()

# ================================
# START FLASK SERVER
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
