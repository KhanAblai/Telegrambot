from services.bot import bot
from telebot.types import *
from services.database import Schedules, find_or_create_user
from datetime import timedelta, datetime


@bot.message_handler(content_types=['text'], regexp='Расписание')
def user_schedules_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    i = 0
    days_buttons = []
    for day in days:
        button = InlineKeyboardButton(day, callback_data='select_day_' + str(i))
        days_buttons.append(button)
        i += 1
    markup.add(*days_buttons)
    today_button = InlineKeyboardButton('Сегодня', callback_data='select_day_today')
    tomorrow_button = InlineKeyboardButton('Завтра', callback_data='select_day_tomorrow')
    markup.add(today_button, tomorrow_button)
    bot.send_message(message.chat.id, text='Выберите день недели', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_day_'), )
def schedule_get(call):
    user = find_or_create_user(call.from_user.id)
    day = call.data.replace('select_day_', '')
    if day == 'today':
        day = datetime.now().day
    if day == 'tomorrow':
        day = (datetime.now() + timedelta(days=1)).day
    print(day, user.group_id)
    Schedules.create(subject_id=1)
    schedule = Schedules.select().where(Schedules.day == int(day), Schedules.group_id == user.group_id.id)
    subjs = ''
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    for item in schedule:
        subject = item.subject_id.name
        lesson_start = item.lesson_start
        lesson_end = item.lesson_end
        print(subject,lesson_end,lesson_start)
        subjs += subject + ': ' + lesson_start + ' - ' + lesson_end + '\n'
    bot.send_message(call.from_user.id, text='Расписание на ' + days[int(day)] + ':\n' + subjs + ' \n' + ' \n')
