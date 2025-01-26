import random
from io import StringIO
# io - это встроенная библиотека Python, i = input o =output
# StringIO - класс для работы со строками в памяти, как с файлами.
# Он позволяет записывать текстовые данные в “виртуальный файл” (хранящийся в оперативной памяти) и считывать их оттуда.

from telebot import TeleBot
from telebot import types # импортировав types - импортируем типы данных из API

import config
import list_of_random_messages
import help_message



bot = TeleBot(config.TOKEN)

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
    # Отправка фото через чтение из файла
    start_photo = types.InputFile('photo/some_photo.jpeg')  # аргументом передается путь к файлу
    bot.send_photo( # Отправляем фото из директории
        chat_id=message.chat.id,
        #photo=start_photo, # отправка самого файла с подгрузкой в телеграм, что не эффективно
        photo=config.some_photo_id,  # отправка фото, которое уже есть на сервере телеграм,
        caption='Смотрите какое фото!'
    )
# Чтобы получить ID фото - нужно bot.send_photo() поместить в переменную (some_w), а потом получит у переменной последний размер
#  some_w.photo[-1], потом копируем ID и используем его

@bot.message_handler(content_types=['photo'])
def echo_photo_handle(message: types.Message):
    text = message.caption
    if message.caption and 'перешли' in text.lower():
        bot.send_photo(
            chat_id=config.group_id, # пересылает фото в заранее созданный чат с записанным в config id
            photo=message.photo[-1].file_id, # у изображения в телеграм существует несколько размеров, берем последний, ибо самый большой
            caption='Ваше фото'
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
        text=help_message.help_message
    )

@bot.message_handler(commands=['random'])
def handle_command_random(message: types.Message):
    user_text = message.text
    bot_answer = random.choice(list_of_random_messages.list_of_messages)
    print(f'Пользователь: {user_text}')
    print(f'Ответ: {bot_answer}')
    bot.send_message(
        chat_id=message.chat.id,
        text=bot_answer
    )

# Отправляет документ по команде
@bot.message_handler(commands=['docs'])
def handle_command_docs(message: types.Message):
    bp_doc = types.InputFile('documents/БП-2.pdf')
    bot.send_document(
        chat_id=message.chat.id,
        document=bp_doc
    )

# Фильтрация через функцию
def is_complete(message: types.Message):
    return message.text and 'готово' in message.text.lower()

@bot.message_handler(func=is_complete)
def handle_complete(message: types.Message):
    bot.send_message(
        chat_id=config.group_id,
        text='Задание выполнено!'
    )


# Отправка сообщения в ответ на сообщение пользователя, если команда не заложена в боте
# Этот обраотчик стоит ставить самым последним обработчиком, иначе алгоритм может остановиться на нем и не дойти до нужного обработчика
@bot.message_handler()
def echo_message(message: types.Message): # обязательно передавать объект message, даже если он не используется и в явном виде указываем тип объекта
    user_text = message.text #  записываем сообщение пользователя в переменную
    print(f'Пользователь: {user_text}') # выводим в консоль сообщение пользователя
    bot_message = 'Я еще не знаю этой команды :( попробуй еще раз'
    print(f'Ответ: {bot_message}')
    bot.send_message(
        chat_id=message.chat.id,  # берем chat_id из сообщения присланного, пользователем
        text=bot_message
    )


# Запускаем long polling только если запускается основной файл, иначе полинг будет выполняться при любом вызове файла, например импорте
if __name__ == '__main__':
    # Запускаем бесконечную связь с сервером, это всегда последняя строка кода
    bot.infinity_polling(skip_pending=True)
    # Передаваемый аргумент skip_pending нужен, чтобы проигнорировать сообщения отправленные боту, пока он был недоступен
    # Бот ответит только на последнее отправленное ему сообщение