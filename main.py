# Импортируем встроенные в Python библиотеки
import random
from io import StringIO # StringIO используется для работы с текстовыми данными в памяти как с файлами. Если нужно работать с бинарными данными, используйте BytesIO из того же модуля.

# Импортируем нужные модули из pyTelegramBotAPI
from telebot import TeleBot
from telebot import types # импортировав types - импортируем типы данных из API
from telebot import custom_filters # импортируем кастомные фильтры
from telebot.types import InputFile

# Импортируем собственные модули
import config
import list_of_random_messages
import help_message
import project_filters
import text_formatting
from config import group_id

bot = TeleBot(config.TOKEN_TEST_BOT) # создаем бота как объект класса Telebot и передаем токен как аргумент
bot.add_custom_filter(custom_filters.IsReplyFilter()) # подключаем кастомный фильтр с проверкой является ли сообщение ответом
bot.add_custom_filter(project_filters.IsUserAdminOfBot()) # подключаем кастомный фильтр из файла project_filters,
# далее в обработчики нужно будет передавать ключ (key) из соответствующего кастомного фильтра в файле project_filters
# в формате key=True или key=False, конкретно в этом примере is_bot_admin=True или is_bot_admin=False
bot.add_custom_filter(project_filters.ContainsWordFilter())

@bot.message_handler(commands=['start'])
def handle_command_start(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text='<b>Привет!</b>', # используем инструмент форматирования текста из import formatting
        parse_mode='HTML', # обозначаем, что текст форматированный, параметр parse_mode обязательный в случае форматирования
    )
    # Отправка фото через чтение из файла
    start_photo = types.InputFile('photo/some_photo.jpeg')  # аргументом передается путь к файлу
    bot.send_photo( # Отправляем фото из директории
        chat_id=message.chat.id,
        #photo=start_photo, # отправка самого файла с подгрузкой в телеграм, что не эффективно
        photo=config.uppetit_logo,  # отправка фото, которое уже есть на сервере телеграм,
        caption='Смотрите какое фото!'
    )

# Фильтрация через функцию и обработчик работающий с текстом
def is_complete(message: types.Message):
    return message.text and 'готово' in message.text.lower()

@bot.message_handler(func=is_complete)
def handle_complete(message: types.Message):
    bot.send_message(
        chat_id=config.group_id,
        text='Задание выполнено!'
    )

# Фильтрация через кастомный фильтр в модуле project_filters.py и обработчик, работающий с фото
@bot.message_handler(content_types=['photo'],contains_word='готово')
def handle_complete(message: types.Message):
    bot.send_message(
        chat_id=config.group_id,
        text='Задание выполнено!'
    )
    bot.send_photo(
        chat_id=config.group_id,
        photo=message.photo[-1].file_id
    )

# Отправляет id фото если получает фото с подписью id
@bot.message_handler(content_types=['photo'], contains_word='id')
def handle_photo_id(message: types.Message):
    photo_id = bot.send_message(
        chat_id=message.chat.id,
        text=f'ID фотографии: <pre>{message.photo[-1].file_id}</pre>',
        parse_mode='HTML'
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

# Обработчик, который пересылает копии сообщения от пользователя в группу
# @bot.message_handler()
# def copy_incoming_message(message: types.Message):
#     bot.copy_message(
#         chat_id=config.group_id,  # куда отправляем копию сообщения
#         from_chat_id=message.chat.id,  # откуда получаем сообщение
#         message_id=message.id
#     )


@bot.message_handler(commands=['help'])
def handle_command_help(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=help_message.help_message,
        parse_mode='HTML'
    )

# По команде формирует в опперативной памяти документ с информацией о пользователе и отправляет пользователю
@bot.message_handler(commands=['me'])
def handle_user_info(message: types.Message):
    file = StringIO()  # создаем объект класса StringIO(), т.е. файл
    file.write('User info:\n')
    file.write('User id: ')
    file.write(str(message.from_user.id))
    file.write('\n')
    file.write('First name: ')
    file.write(str(message.from_user.first_name))
    file.write('\n')
    file.write('Last name: ')
    file.write(str(message.from_user.last_name))
    file.write('\n')
    file.write('Username: ')
    file.write(str(message.from_user.username))
    file.write('\n')
    file.seek(0) # после записи инфо в файл обязательно возвращаем курсор в начало файла, иначе выдаст ошибку, что файл пустой
    file_text_doc = types.InputFile(file)  # читаем файл и помещаем в переменную
    bot.send_document(   # отправляем файл
        chat_id=message.chat.id,
        document=file_text_doc,
        visible_file_name='Ваши данные',
        caption='Вот ваши данные'
    )




@bot.message_handler(commands=['random'])
def handle_command_random(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=random.choice(list_of_random_messages.list_of_messages)
    )

# Отправляет документ по команде
@bot.message_handler(commands=['docs'])
def handle_command_docs(message: types.Message):
    bp_doc = types.InputFile('documents/БП-2.pdf')
    bot.send_document(
        chat_id=message.chat.id,
        document=bp_doc
    )

# Обработчик, который позволяет админу группы получить id группы
@bot.message_handler(commands=['chat_id'], is_bot_admin=True) # is_bot_admin идет из модуля project_filters.py
def handle_chat_id_admin_request(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f'ID пользователя: <pre>{message.from_user.id}</pre>\n\nID чата: <pre>{message.chat.id}</pre>',
        parse_mode='HTML',
        reply_to_message_id=message.id
    )

# Обработчик, который выдает ошибку, если обычный пользователь пытается использовать команду только для админов
@bot.message_handler(commands=['chat_id'], is_bot_admin=False)
def handle_chat_id_user_request(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f'У @{message.from_user.username} нет доступа к команде chat_id'
    )


content_types_to_ru = {
    'text': 'текст',
    'photo': 'фото',
    'sticker': 'стикер',
    'document': 'документ'
}

# Обработчик для ответа на сообщение на которое ответил пользователь
@bot.message_handler(is_reply=True)
def handle_reply_message(message: types.Message):
    message_type = message.reply_to_message.content_type
    if message_type in content_types_to_ru:
        message_type = content_types_to_ru[message_type]
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Вы ответили на это сообщение, <b>тип контента</b>: {message_type}',   # используем простейший способ форматирования текста
        reply_to_message_id=message.reply_to_message.id,
        parse_mode='HTML'  # обозначаем, что текст форматированный, параметр parse_mode обязательный в случае форматирования
    )

@bot.message_handler(commands=['formatting'])
def hendle_formatting_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=text_formatting.text_f,
        parse_mode='HTML'
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