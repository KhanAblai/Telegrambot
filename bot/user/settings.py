from services.bot import bot
from telebot.types import *
from services.database import find_or_create_user


@bot.message_handler(content_types='text', regexp='Настройки')
def change_settings(message):
    markup = InlineKeyboardMarkup()
    noti_on = InlineKeyboardButton(text='Включить уведомления', callback_data='noti_on')
    noti_off = InlineKeyboardButton(text='Выключить уведомления', callback_data='noti_off')
    markup.add(noti_on, noti_off)
    bot.send_message(message.chat.id, text='Выберите состояние уведомлений', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('noti_'), )
def changed_settings(call):
    user = find_or_create_user(call.from_user.id)
    notif = call.data.replace('noti_', '')
    user.notification = notif == 'on'
    user.save()
