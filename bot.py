import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

history = []

suits = ['♠️','♥️','♦️','♣️']

suit_map = {
    "пик": "♠️",
    "черви": "♥️",
    "буби": "♦️",
    "треф": "♣️",
    "♠️": "♠️",
    "♥️": "♥️",
    "♦️": "♦️",
    "♣️": "♣️"
}

def analyze(history):
    total = len(history)
    counts = {s: history.count(s) for s in suits}

    # вероятность
    probs = {s: int((counts[s]/total)*100) for s in suits}

    # скоринг
    scores = {}
    for s in suits:
        score = 0
        score += (10 - counts[s]) * 2
        score += (5 - history[-5:].count(s)) * 3
        scores[s] = score

    best = max(scores, key=scores.get)
    second = sorted(scores, key=scores.get, reverse=True)[1]

    # уверенность
    if probs[best] > 55:
        conf = "ЖОҒАРЫ"
    elif probs[best] > 40:
        conf = "ОРТА"
    else:
        conf = "ТӨМЕН"

    return best, second, probs, conf


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Маст жібер: пик / черви / буби / треф")


@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.lower()

    if text in suit_map:
        history.append(suit_map[text])

        if len(history) >= 5:
            best, second, probs, conf = analyze(history)

            msg = f"""📊 Анализ масти

🎯 Негізгі: {best}
⚡ Альтернатива: {second}

📈 Вероятность:
♠️ — {probs['♠️']}%
♥️ — {probs['♥️']}%
♦️ — {probs['♦️']}%
♣️ — {probs['♣️']}%

📊 Уверенность: {conf}
"""
            bot.send_message(message.chat.id, msg)

        else:
            bot.send_message(message.chat.id, "Тағы жібер (кемі 5)")
    else:
        bot.send_message(message.chat.id, "пик / черви / буби / треф деп жаз")

bot.infinity_polling()
