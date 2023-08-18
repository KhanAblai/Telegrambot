from services.bot import bot
from telebot.types import *
from services.database import Groups, Subjects, Schedules
from services.helpers import add_minutes_to_time, days
from . import menu


@bot.callback_query_handler(func=lambda call: call.data.startswith('schedule_change'))
def handle_schedule_change(call):
    show_groups(call.from_user.id)


def show_groups(telegram_id):
    groups = Groups.select()
    markup = InlineKeyboardMarkup()
    for group in groups:
        print('генерируем кнопки с группами ' + str(group.id))
        markup.add(InlineKeyboardButton(group.name, callback_data=f'group_id_schedule_change_{group.id}'))
    bot.send_message(telegram_id, text='Выберите группу ', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_id_schedule_change_'))
def handle_group_selection(call):
    group_id = call.data.replace('group_id_schedule_change_', '')
    show_week_days(call.from_user.id, group_id)


def show_week_days(telegram_id, group_id):
    markup = InlineKeyboardMarkup()
    i = 0
    for day in days:
        markup.add(InlineKeyboardButton(day, callback_data=f'select_day_schedule_change_{i}_{group_id}'))
        i += 1
    bot.send_message(telegram_id, text='Выберите день недели', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('select_day_schedule_change'))
def handle_day_selection(call):
    day_and_group_id = call.data.replace('select_day_schedule_change', '')
    day_and_group_id_arr = day_and_group_id.split('_')
    day = int(day_and_group_id_arr[0])
    group_id = int(day_and_group_id_arr[1])
    show_subject_change_menu(call.from_user.id, day, group_id)


def show_subject_change_menu(telegram_id, day, group_id):
    schedule = Schedules.select().where(Schedules.day == day, Schedules.group_id == group_id)
    markup = InlineKeyboardMarkup()
    for item in schedule:
        markup.add(InlineKeyboardButton(item.subject_id.name, callback_data=f'select_subject_{item.id}'))
    markup.add(InlineKeyboardButton('Добавить предмет', callback_data=f'subject_add_{group_id}_{day}'))
    bot.send_message(telegram_id, text='Выберите предметы', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('sch_subject_add_'))
def schedule_subject_add(call):
    print('Выбрали добавление', call.data)
    sch_rep = call.data.replace('sch_subject_add_', '')
    sch_arr = sch_rep.split('_')
    group_id = sch_arr[0]
    print('Получаем груп айди в добавлении предмета', group_id)
    day = sch_arr[1]
    subjects = Subjects.select()
    markup = InlineKeyboardMarkup()
    for item in subjects:
        print('Итерация добавления предмета', 'sbj_select_' + str(item.id) + '_' + group_id + '_' + day)
        markup.add(
            InlineKeyboardButton(item.name, callback_data='sbj_select_' + str(item.id) + '_' + group_id + '_' + day))
    bot.send_message(call.from_user.id, text='Выберите предмет который хотите добавить', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sch_subject_update'))
def schedule_subject_update(call):
    subject_id = call.data.replace('sch_subject_update', '')
    handler_ask_lesson_start(subject_id)





@bot.callback_query_handler(func=lambda call: call.data.startswith('subject_'))
def subject_update_or_delete(call):
    print('Выбрали предмет', call.data)
    schedule_id = call.data.replace('subject_', '')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Удалить', callback_data='sch_subject_delete' + schedule_id))
    markup.add(InlineKeyboardButton('Изменить', callback_data='sch_subject_update' + schedule_id))
    bot.send_message(call.from_user.id, text='Выберите действие', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sch_subject_delete'))
def subject_delete(call):
    print('Выбрали удаление')
    schedule_id = call.data.replace('sch_subject_delete', '')
    schedule = Schedules.get(Schedules.id == schedule_id)
    schedule.delete_instance()
    bot.send_message(call.from_user.id, text='Удален предмет ' + str(schedule.subject_id.name))
    menu.show_admin_menu(call.from_user.id)


def handler_change_lesson_time(message, id):
    schedul = Schedules.get(Schedules.id == id)
    new_lesson_start_time = message.text  # 9:00
    schedul.lesson_start = new_lesson_start_time
    schedul.lesson_end = add_minutes_to_time(new_lesson_start_time, 90)
    schedul.save()
    bot.send_message(message.from_user.id,
                     text=f'Изменения были сохранены,время начало и конца установлены как {schedul.lesson_start} - {schedul.lesson_end}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('sbj_select_'))
def handler_ask_lesson_start(call):
    try:
        sch_rep = call.data.replace('sbj_select_', '')
        sch_arr = sch_rep.split('_')
        subject_id = sch_arr[0]
        group_id = sch_arr[1]
        print('Узнаем лесон старт груп айди', group_id)
        day = sch_arr[2]
        print(sch_arr)
        schedule = Schedules.create(day=day, group_id=group_id, subject_id=subject_id)
        message = bot.send_message(call.from_user.id, text='Введите новое время для урока в формате ЧЧ:мм,пример 09:00')
        bot.register_next_step_handler(message, lambda message: handler_change_lesson_time(message, schedule.id))
    except Exception:
        subj_id = call
        schedule = Schedules.get(Schedules.id == subj_id)
        message = bot.send_message(call.from_user.id, text='Введите новое время для урока в формате ЧЧ:мм,пример 09:00')
        bot.register_next_step_handler(message, lambda message: handler_change_lesson_time(message, schedule.id))
