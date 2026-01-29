# ================================
# 🌍 GEOPOLITICAL TELEGRAM BOT (RENDER FIXED)
# ================================

import logging
import requests
import feedparser
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import re
import datetime
import os

# ================================
# 🔑 YOUR TELEGRAM BOT TOKEN
# ================================
BOT_TOKEN ="8547149588:AAE2XmSZsjHgX6fKzrXxQDwobWV9UCzValM"

# ================================
# 🌐 KEEP-ALIVE WEB SERVER (RENDER)
# ================================
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "🌍 Geopolitical Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()

# ================================
# 📰 NEWS ANALYSIS ENGINE
# ================================
def get_news_score(query):
    try:
        url = f"https://news.google.com/rss/search?q={query}+war"
        feed = feedparser.parse(url)
        articles = feed.entries[:8]

        score = 0
        high = ["war", "attack", "strike", "invasion", "military", "missile"]
        mid = ["tension", "sanction", "threat", "conflict", "troops"]

        for a in articles:
            title = a.title.lower()
            if any(k in title for k in high):
                score += 2
            elif any(k in title for k in mid):
                score += 1

        return min(score, 10)
    except:
        return 2

# ================================
# 🧠 GEO LOGIC SCORES
# ================================
def reality_score(q):
    q = q.lower()
    if "invade" in q or "war" in q:
        return 2
    return 5

def military_score(q):
    return 3 if "war" in q or "invade" in q else 2

def time_score(q):
    if re.search(r"by\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", q.lower()):
        return 2
    return 5

def market_score(q):
    return 4 if "war" in q or "invade" in q else 5

def chaos_score():
    return 4

# ================================
# 📊 PROBABILITY ENGINE
# ================================
def calculate_probability(R, N, M, P, T, C):
    raw = (
        R * 0.20 +
        N * 0.15 +
        M * 0.25 +
        P * 0.15 +
        T * 0.15 +
        C * 0.10
    ) * 10

    final_prob = raw * 0.3  # war rarity filter
    return round(final_prob, 2)

# ================================
# 💰 TRADING DECISION
# ================================
def trading_decision(prob):
    if prob > 60:
        return "🟢 BUY YES", "$120–160"
    elif prob < 30:
        return "🔴 BUY NO", "$120–150"
    else:
        return "🟡 WAIT", "$0–50"

# ================================
# 🤖 TELEGRAM COMMAND
# ================================
async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text("❗ Example:\n/geo Will US invade Venezuela?")
        return

    R = reality_score(question)
    N = get_news_score(question)
    M = military_score(question)
    P = market_score(question)
    T = time_score(question)
    C = chaos_score()

    prob = calculate_probability(R, N, M, P, T, C)
    decision, capital = trading_decision(prob)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    reply = f"""
🌍 GEOPOLITICAL INTELLIGENCE REPORT

❓ Question:
{question}

🕒 Time: {now}

🧠 Scores (0–10):
Reality: {R}/10
News: {N}/10
Military: {M}/10
Market: {P}/10
Time Logic: {T}/10
Chaos Risk: {C}/10

📊 Probability:
➡️ {prob}%

💰 Trading Decision:
➡️ {decision}
💵 Suggested Capital: {capital}

⚠️ Analysis only, not financial advice.
"""
    await update.message.reply_text(reply)

# ================================
# 🚀 START BOT (RENDER SAFE)
# ================================
async def main():
    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("geo", geo))

    print("🌍 Geopolitical Bot started on Render...")

    await app.initialize()
    await app.start()
    await app.bot.delete_webhook(drop_pending_updates=True)  # IMPORTANT FIX
    await app.stop()  # prevent webhook conflict
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

