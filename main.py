import telebot as telebot

bot = telebot.TeleBot('TOKEN')


def greeting(message):
    if message.from_user.first_name and message.from_user.last_name:
        return f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}!'
    if message.from_user.first_name:
        return f'Здравствуйте, {message.from_user.first_name}!'
    if message.from_user.last_name:
        return f'Здравствуйте, {message.from_user.last_name}!'
    return f'Здравствуйте!'


@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(message)

    if message.text.strip().lower() in ('/start', 'go', 'начать'):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Найти песню')
        markup.add(photo)
        bot.send_message(message.chat.id, greeting(message), reply_markup=markup)

    elif text.isdigit() and 0 < int(text) < 1001:
        file_name = f'songs/{int(text)}.txt'
        f = open(file_name, 'r')
        s = f.read()
        bot.send_message(message.chat.id, f'{s}')

    else:
        bot.send_message(message.chat.id, f'Введите номер песни (число от 1 до 1000)')


print('bot is started')
bot.polling(none_stop=True)
