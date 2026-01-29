# ================================
# 🌍 GEOPOLITICAL AI TELEGRAM BOT
# ================================

import requests
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import re
import datetime

# ================================
# 🔑 YOUR TELEGRAM BOT TOKEN
# ================================
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

# ================================
# 🌐 KEEP-ALIVE WEB SERVER (24/7)
# ================================
web_app = Flask("geo_bot")

@web_app.route("/")
def home():
    return "🌍 Geopolitical Bot is running 24/7!"

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()

# ================================
# 📰 NEWS ANALYSIS ENGINE
# ================================
def get_news_score(query):
    try:
        url = f"https://news.google.com/rss/search?q={query}+geopolitics"
        feed = feedparser.parse(url)
        articles = feed.entries[:8]

        score = 0
        keywords_high = ["war", "attack", "strike", "invasion", "military", "missile"]
        keywords_mid = ["tension", "sanction", "threat", "conflict", "troops"]

        for a in articles:
            title = a.title.lower()
            if any(k in title for k in keywords_high):
                score += 2
            elif any(k in title for k in keywords_mid):
                score += 1

        return min(score, 10)
    except:
        return 2

# ================================
# 🪖 MILITARY SIGNAL ENGINE (LOGIC)
# ================================
def military_score(question):
    q = question.lower()
    if any(word in q for word in ["invade", "war", "attack"]):
        return 3  # wars are hard to start suddenly
    return 2

# ================================
# 🧠 REALITY SCORE (GEOPOLITICS LOGIC)
# ================================
def reality_score(question):
    q = question.lower()

    hard_events = ["invade", "full war", "nuclear"]
    medium_events = ["strike", "military action", "sanctions"]

    if any(e in q for e in hard_events):
        return 2
    if any(e in q for e in medium_events):
        return 4
    return 5

# ================================
# ⏳ TIME LOGIC SCORE
# ================================
def time_score(question):
    q = question.lower()

    # If question mentions short deadline
    if re.search(r"by\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", q):
        return 2
    return 5

# ================================
# 🐋 POLYMARKET / MARKET SIGNAL LOGIC (SIMPLIFIED)
# ================================
def market_score(question):
    # Real logic: geopolitics markets usually exaggerate war
    q = question.lower()
    if "invade" in q or "war" in q:
        return 4  # markets hype wars
    return 5

# ================================
# 🌪️ CHAOS RISK SCORE
# ================================
def chaos_score():
    # geopolitics always has uncertainty
    return 4

# ================================
# 📊 PROBABILITY ENGINE (REAL MODEL)
# ================================
def calculate_probability(R, N, M, P, T, C):
    raw = (
        R * 0.20 +
        N * 0.15 +
        M * 0.25 +
        P * 0.15 +
        T * 0.15 +
        C * 0.10
    ) * 10  # convert to %

    # Extreme geopolitics filter (war/invasion are rare)
    final_prob = raw * 0.3
    return round(final_prob, 2)

# ================================
# 💰 TRADING DECISION ENGINE
# ================================
def trading_decision(prob):
    if prob > 60:
        return "🟢 BUY YES", "$120–160"
    elif prob < 30:
        return "🔴 BUY NO", "$120–150"
    else:
        return "🟡 WAIT", "$0–50"

# ================================
# 🤖 TELEGRAM COMMAND: /geo
# ================================
async def geo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)

    if not question:
        await update.message.reply_text(
            "❗ Example:\n/geo Will the US invade Venezuela by Jan 31?"
        )
        return

    # Scores
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
News Strength: {N}/10
Military Signals: {M}/10
Market/Polymarket: {P}/10
Time Logic: {T}/10
Chaos Risk: {C}/10

📊 Final Probability:
➡️ {prob}%

💰 Trading Decision:
➡️ {decision}
💵 Suggested Capital (for $200): {capital}

🧠 Interpretation:
- <30% = Market overhyping event
- 30–60% = Uncertain risk
- >60% = Serious geopolitical escalation

⚠️ This is analytical intelligence, not financial advice.
"""

    await update.message.reply_text(reply)

# ================================
# 🚀 START BOT
# ================================
def main():
    app = ApplicationBuilder().token().build()
    app.add_handler(CommandHandler("geo", geo))
    print("🌍 Geopolitical AI Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
