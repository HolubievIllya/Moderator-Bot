import telebot
import time
import string
import os
from dotenv import load_dotenv


bot = telebot.TeleBot(os.getenv("TG_TOKEN"))

load_dotenv()
messages = {}

def count_words(lst):
    counts = []
    for i in lst:
        if i[0] not in counts:
            counts.append(i[0])
            counts.append(1)
        else:
            counts[counts.index(i[0])+1] += 1
    return counts

@bot.message_handler(commands=['rules'])
def rules(message):
    print("rules")
    bot.reply_to(message, "👮‍♂️<b>Правила чата:</b> \n"
                 "Запрещено:\n"
                 "— Оскорбления участников чата\n"
                 "— Флуд, флейм, спам и чрезмерный оффтоп\n"
                 "— Беспричинная отправка гиф, стикеров\n"
                 "— Разжигание ненависти к любым рассам/национальностям <i>(кроме руских свинок)</i>/ориентациям и другим подобным признакам\n",  parse_mode='HTML')

@bot.message_handler(content_types=[
    "new_chat_members"
])
def foo(message):
    print(message)
    print(message.from_user.id)
    chat_id = message.chat.id
    bot.send_message(chat_id, "<b>Добро пожаловать в наш чат</b> 👋 @" + message.from_user.username + " Чем вы занимались сегодня? \n<i>посмотреть правила /rules</i>", parse_mode='HTML')
    # bot.delete_message(chat_id, message)
    # bot.reply_to(message, "welcome") реплай на сообщение от


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(2)
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = message.from_user.username
    message_text = message.text.lower().translate(str.maketrans("", "", string.punctuation))
    message_time = time.time()
    messages.setdefault(user_id, []).append((message_text, message_time))
    messages[user_id] = [(m, t) for (m, t) in messages[user_id] if time.time() - t < 60]
    count_messages = count_words(messages[user_id])
    if int(max(count_messages[1::2])) > 4:
        # Отправка сообщения пользователю о муте на час
        try:
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + 3600)
            bot.send_message(chat_id, "Пользователь @" + user + " был замучен на 1 час за спам, старайтесь больше не нарушать правила.")
            bot.send_message(chat_id, "Первый мут на час, следующий мут будет на день")
        except telebot.apihelper.ApiTelegramException:
            print("Ошибка, я не могу замутить администратора.")
        # Отправка сообщения администратору о количестве сообщений пользователя
        try:
            bot.send_message(693188597, 'У пользователя с ником @' + user + " больше 4 сообщений '" + str(count_messages[count_messages.index(max(count_messages[1::2]))-1]) + "' за минуту, он был замучен.")
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отправить сообщение вам в ЛС, убедитесь что уже писали данному боту в личку.")




bot.polling(none_stop=True)