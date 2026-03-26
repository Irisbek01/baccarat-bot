import telebot
from collections import Counter
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

history = []

def get_strike_bonus(history, suit):
    streak = 0
    for h in reversed(history):
        if h == suit:
            streak += 1
        else:
            break
    return -streak * 2

def weighted_score(history, suit):
    score = 0
    count = history.count(suit)
    score += (10 - count)
    last10 = history[-10:]
    score += (10 - last10.count(suit)) * 2
    score += get_strike_bonus(history, suit)
    return score

def predict_best(history):
    suits = ['♠️','♥️','♦️','♣️']
    scores = {s: weighted_score(history, s) for s in suits}
    return max(scores, key=scores.get)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 МАСТ БОТ 24/7\nМаст жибер ♠️ ♥️ ♦️ ♣️")

@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.strip()
    
    if text in ['♠️','♥️','♦️','♣️']:
        history.append(text)
        
        if len(history) >= 5:
            best = predict_best(history)
            bot.send_message(message.chat.id, f"🎯 {best}")
        else:
            bot.send_message(message.chat.id, "Тағы жібер (кемі 5)")
    else:
        bot.send_message(message.chat.id, "Тек маст!")

bot.infinity_polling()
