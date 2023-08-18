import telebot
import threading

bot = telebot.TeleBot('6100467536:AAEzWWz0-2nRUCgPmy-P2LbVAZFCmRETBSs')


def bot_loop():
    print('bot_loop started')
    bot.polling(none_stop=True)


t = threading.Thread(target=bot_loop)
t.start()
print('bot initialized')