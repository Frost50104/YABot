from telebot import TeleBot

# вынести в отдельный файл
TOKEN = '7464601268:AAGo5B-_NLEM57sockMAUkhRk_Av76FJtIM'
CHAT_ID = 854825784

bot = TeleBot(TOKEN)

message_1 = bot.send_message(chat_id=CHAT_ID, text='Привет из Pycharm!')

