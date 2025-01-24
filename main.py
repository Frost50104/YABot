from telebot import TeleBot, types # импортировав types - импортируем типы данных из API
from config import TOKEN


help_message = """ Вот список доступных команд:
/start - начало работы с ботом
/help - показать список команд 
"""
# команды надо прописывать в бот через BotFather через команду /setcommands

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_command_start(message: types.Message):
    user_text = message.text
    bot_answer = 'Привет!'
    print(f'Пользователь: {user_text}')
    print(f'Ответ: {bot_answer}')
    bot.send_message(
        chat_id=message.chat.id,
        text=bot_answer
    )

@bot.message_handler(commands=['help'])
def handle_command_help(message: types.Message):
    user_text = message.text
    bot_answer = help_message
    print(f'Пользователь: {user_text}')
    print(f'Ответ: {bot_answer}')
    bot.send_message(
        chat_id=message.chat.id,
        text=help_message
    )


# Отправка сообщения в ответ на сообщение пользователя
@bot.message_handler()
def echo_message(message: types.Message): # обязательно передавать объект message, даже если он не используется и в явном виде указываем тип объекта
    user_text = message.text #  записываем сообщение пользователя в переменную
    print(f'Пользователь: {user_text}') # выводим в консоль сообщение пользователя
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