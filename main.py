from telebot import TeleBot, types # импортировав types - импортируем типы данных из API

# вынести в отдельный файл
TOKEN = '7464601268:AAGo5B-_NLEM57sockMAUkhRk_Av76FJtIM'

bot_commands = ['/start','/help']

bot = TeleBot(TOKEN)

# Отправка сообщения в ответ на сообщение пользователя
@bot.message_handler()
def reply_send_message(message: types.Message): # обязательно передавать объект message, даже если он не используется и в явном виде указываем тип объекта
    user_text = message.text #  записываем сообщение пользователя в переменную
    print(f'Пользователь: {user_text}') # выводим в консоль сообщение пользователя
    if user_text == bot_commands[0]: # условие при котором бот отправит сообщение в ответ пользователю
        bot_message = 'Привет я проект бота!'
        print(f'Ответ: {bot_message}')
    elif user_text == bot_commands[1]:
        bot_message = f'Вот список команд: {bot_commands}'
        print(f'Ответ: {bot_message}')
    else:
        bot_message = 'Я еще не знаю этой команды :('
        print(f'Ответ: {bot_message}')
    bot.send_message(
        chat_id=message.chat.id,  # берем chat_id из сообщения присланного, пользователем
        text=bot_message
    )

# if 'текст' in user_text.lower(): # если сообщение пользователя хоть где-то содержит "текст"
#     bot.send_message(
#         chat_id=message.chat.id,  # берем chat_id из сообщения присланного, пользователем
#         text='ответ'
#     )

# Запускаем бесконечную связь с сервером, это всегда последняя строка кода
bot.infinity_polling()