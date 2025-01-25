from telebot import TeleBot, types # импортировав types - импортируем типы данных из API
from config import TOKEN
from list_of_random_messages import list_of_messages
from help_message import help_message
import random


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
    # Открытие фото в режиме чтения байтов
    with open('some_photo.jpeg', 'rb') as some_photo:
        bot.send_photo( # Отправляем фото из директории
            chat_id=message.chat.id,
            photo=some_photo,
            caption='Смотрите какое фото!'
        )

@bot.message_handler(content_types=['photo'])
def echo_photo_handle(message: types.Message):
    text = message.caption
    if message.caption and 'перешли' in text.lower():
        bot.send_photo(
            chat_id=message.chat.id,
            photo=message.photo[-1].file_id # у изображения в телеграм существует несколько размеров, берем последний, ибо самый большой
        )
    else:
        user_text = message.photo
        bot_answer = 'Это фото!'
        print(f'Пользователь: {user_text}')
        print(f'Ответ: {bot_answer}')
        bot.send_message(
            chat_id=message.chat.id,
            text=bot_answer,
            reply_to_message_id=message.id  # аргумент, чтобы бот отправил ответ на сообщение, а не просто сообщение
        )
        bot.send_sticker(  # бот отправляет стикер
            chat_id=message.chat.id,
            sticker='CAACAgIAAxkBAAEBBHtnlJVoKmN-hhpOiZNFWw9aphHH9wACFQADwDZPE81WpjthnmTnNgQ',
            reply_to_message_id=message.id
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

@bot.message_handler(commands=['random'])
def handle_command_random(message: types.Message):
    user_text = message.text
    bot_answer = random.choice(list_of_messages)
    print(f'Пользователь: {user_text}')
    print(f'Ответ: {bot_answer}')
    bot.send_message(
        chat_id=message.chat.id,
        text=bot_answer
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

# Запускаем long polling только если запускается основной файл, иначе полинг будет выполняться при любом вызове файла, например импорте
if __name__ == '__main__':
    # Запускаем бесконечную связь с сервером, это всегда последняя строка кода
    bot.infinity_polling(skip_pending=True)
    # Передаваемый аргумент skip_pending нужен, чтобы проигнорировать сообщения отправленные боту, пока он был недоступен
    # Бот ответит только на последнее отправленное ему сообщение