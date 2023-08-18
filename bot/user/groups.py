from services.bot import bot
from telebot.types import *
from services.database import get_groups, save_group_info
from . import menu

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_group'))
def handle_change_user_group(call):
    print('Вызов select_group')
    group_id = call.data.replace("select_group_", "")
    save_group_info(call.from_user.id, group_id)
    menu.show_main_menu(call.from_user.id)


@bot.message_handler(content_types='text', regexp='Сменить группу')
def group_change_menu(message):
    markup = InlineKeyboardMarkup()
    groups = get_groups()
    for group in groups:
        markup.add(InlineKeyboardButton(group.name, callback_data='select_group_' + str(group.id)))
    bot.send_message(message.chat.id, text='Выберите группу на которую хотите сменить', reply_markup=markup)
