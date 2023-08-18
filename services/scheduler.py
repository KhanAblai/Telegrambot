import schedule
import time
import threading


def async_loop():
    print('schedule_loop запущен')
    while True:
        schedule.run_pending()
        time.sleep(1)


t = threading.Thread(target=async_loop)
t.start()
print('scheduler инициализирован')
