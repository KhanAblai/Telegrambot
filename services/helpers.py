import datetime
from datetime import timedelta, datetime


days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']


def add_minutes_to_time(time_string: str, minutes: int) -> str:
    time_format = "%H:%M"
    time_object = datetime.strptime(time_string, time_format)
    new_time_object = time_object + timedelta(minutes=minutes)
    new_time_string = new_time_object.strftime(time_format)
    return new_time_string
