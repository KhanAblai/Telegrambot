from services.scheduler import schedule
from services.database import Schedules, Users
from services.bot import bot
import time


def next_lesson_start_notification():
    ten_minutes_before = time.strftime('%H:%M', time.localtime(time.mktime(time.localtime()) + 10 * 60))
    print(ten_minutes_before)
    schedule = Schedules.select().where(Schedules.day == time.localtime().tm_wday,
                                        Schedules.lesson_start == ten_minutes_before)
    for item in schedule:
        message = 'Урок ' + item.subject_id.name + ' начинается через 10 минут'
        users = Users.select().where(Users.group_id == item.group_id)
        for user in users:
            try:
                bot.send_message(user.telegram_id, text=message)
            except Exception:
                print('Ошибка')


def current_lesson_end_notification():
    five_minutes_later = time.strftime('%H:%M', time.localtime(time.mktime(time.localtime()) + 5 * 60))
    print(time.localtime().tm_wday)
    print(five_minutes_later)
    schedule = Schedules.select().where(Schedules.lesson_end == five_minutes_later,
                                        Schedules.day == time.localtime().tm_wday)
    for item in schedule:
        message = 'Урок ' + item.subject_id.name + ' заканчивается через 5 минут'
        users = Users.select().where(Users.group_id == item.group_id)
        for user in users:
            try:
                bot.send_message(user.telegram_id, text=message)
            except Exception:
                print('Ошибка')


schedule.every().minute.at(':00').do(current_lesson_end_notification)
schedule.every().minute.at(':00').do(next_lesson_start_notification)
