# Проверка пользователя на статус админа бота через кастомный фильтр SimpleCustomFilter

# Алгоритм создания кастомного фильтра:
# 1. В файле с фильтрами (project_filters.py) импортировать класс фильтров из pyTelegramBotAPI
# 2. Создать свой класс кастомный фильтр, унаследовав класс из шага №1
# 3. Прописать в своем классе key, который пойдет аргументов в обработчик и функцию проверки (def check)
# 4. Подключить кастомный фильтр в основном файле, пример: bot.add_custom_filter(project_filters.IsUserAdminOfBot())
# 5. Передать в декоратор обработчика в качестве параметра ключевое слово и булевое значение, пример: @bot.message_handler(commands=['chat_id'], is_bot_admin=True)

from telebot.custom_filters import SimpleCustomFilter # шаг №1
from telebot.custom_filters import AdvancedCustomFilter # шаг №1
from telebot.types import Message
import config

# кастомный фильтр, который позволяет делать обработчики для админов и не админов
class IsUserAdminOfBot(SimpleCustomFilter):
    key = 'is_bot_admin'

    def check(self, message: Message):
        return message.from_user.id in config.BOT_ADMIN_USER_IDS


class ContainsWordFilter(AdvancedCustomFilter):
    key = 'contains_word'

    def check(self, message: Message, word: str) -> bool:
        text = message.text or message.caption
        if not text:
            return False
        return word in text.lower()