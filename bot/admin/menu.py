from telebot.types import *
from services.bot import bot


def show_admin_menu(telegram_id):
    markup = InlineKeyboardMarkup()
    group_add = InlineKeyboardButton('Добавление группы', callback_data='group_add')
    schedule_change = InlineKeyboardButton('Изменение расписания', callback_data='schedule_change')
    markup.add(group_add, schedule_change)
    bot.send_message(telegram_id, text='Выберите действие', reply_markup=markup)


@bot.message_handler(content_types='text', regexp='123321')
def handle_admin_password(message):
    show_admin_menu(message.from_user.id)
