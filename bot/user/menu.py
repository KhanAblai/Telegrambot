from services.bot import bot
from telebot.types import *
from services.database import get_groups, find_or_create_user


@bot.message_handler(commands=['start'])
def start(message):
    user = find_or_create_user(message.from_user.id)
    print(user.group_id)
    if user.group_id is not None:
        show_main_menu(message.from_user.id)
    else:
        markup = InlineKeyboardMarkup()
        print('before select')
        groups = get_groups()
        print(groups)
        for group in groups:
            markup.add(InlineKeyboardButton(group.name, callback_data='select_group_' + str(group.id)))
        bot.send_message(message.chat.id, text='Выберите свою группу', reply_markup=markup)


def show_main_menu(telegram_id):
    markup = ReplyKeyboardMarkup()
    user = find_or_create_user(telegram_id)
    print(telegram_id)
    btn1 = KeyboardButton('Расписание')
    btn2 = KeyboardButton('Сменить группу')
    btn3 = KeyboardButton('Настройки')
    markup.add(btn1, btn2, btn3)
    bot.send_message(telegram_id, text='Ваша группа ' + user.group_id.name, reply_markup=markup)
