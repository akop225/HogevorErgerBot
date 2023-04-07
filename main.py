import telebot as telebot

bot = telebot.TeleBot('6217123349:AAFAC4E41Sj9-eHYVX2nSyv8D6wpo09zfgs')

@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(message)

    if message.text.strip().lower() in ('/start', 'go', 'начать'):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Найти песню')
        new_price = telebot.types.KeyboardButton('Создать информацию о товаре')
        markup.add(photo, new_price)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!', reply_markup=markup)

    print(text)
    print(text.isdigit() and 0 < int(text) < 1000)

    if text.isdigit() and 0 < int(text) < 1000:
        file_name = f'songs/{int(text)}.txt'
        f = open(file_name, 'r')
        s = f.read()
        bot.send_message(message.chat.id, f'{s}')


bot.polling(none_stop=True)