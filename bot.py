
suit_map = {
    "пик": "♠️",
    "пики": "♠️",
    "♠️": "♠️",

    "черви": "♥️",
    "червый": "♥️",
    "♥️": "♥️",

    "буби": "♦️",
    "бубный": "♦️",
    "♦️": "♦️",

    "треф": "♣️",
    "крести": "♣️",
    "♣️": "♣️"
}

text = message.text.strip().lower()

if text in suit_map:
    suit = suit_map[text]
    history.append(suit)

    if len(history) >= 5:
        best = predict_best(history)
        bot.send_message(message.chat.id, f"🎯 {best}")
    else:
        bot.send_message(message.chat.id, "Тағы жібер (кемі 5)")
else:
    bot.send_message(message.chat.id, "пик / черви / буби / треф деп жаз")
