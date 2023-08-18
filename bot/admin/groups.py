from services.bot import bot
from services.database import Groups
from bot.admin import menu
@bot.callback_query_handler(func=lambda call: call.data.startswith('group_add'), )
def handle_group_add(call):
    message = bot.send_message(call.from_user.id, text='Напишите название группы,которую хотите добавить')
    bot.register_next_step_handler(message, handle_group_name)


def handle_group_name(message):
    new_group = message.text
    Groups.create(name=new_group)
    bot.send_message(message.from_user.id, text='Новая группа' + new_group)
    menu.show_admin_menu(message.from_user.id)