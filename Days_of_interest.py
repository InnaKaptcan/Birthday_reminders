import datetime
from datetime import datetime as dt
from datetime import timedelta

from Lead_preferences import fridays_before_public_holidays_2023,\
    first_working_day_after_holidays_2023


# ----------День генерации напоминаний-----------
todayis = {'date': datetime.date.today(), 'weekday': dt.today().weekday()}   # сегодняшний
todayis = {'date': datetime.date.today() - timedelta(days=1), 'weekday': dt.today().weekday() - 1}  # вчерашний

# Если ДЕНЬ ВЫБИРАЕТСЯ ВРУЧНУЮ, РАСКОММЕНТИТЬ СЛЕДУЮЩУЮ СТРОКУ
# todayis = {'date': datetime.date(2023, 4, 7), 'weekday': 5} # Департаменты, которые начинаются с 0 / руководитель в 7 отделении
# todayis = {'date': datetime.date(2023, 4, 10), 'weekday': 0}

# Название 1С таблицы именинников
todays_file_name = todayis['date'].strftime("%Y%m%d")

# Специальный день - это день, когда надо проверять не только сегодняшние ДР (перед и после выходными).
Spcl_day = False
# Какие дни оставлять? Как минимум сегодняшний день.
days = [todayis['date'].strftime("%d.%m.%Y")[:5]]
# Если пятница, проверяем на 2 дня вперед + проверям понедельник и вторик, если это выходные
if todayis['weekday'] == 4:
    Spcl_day = True
    for i in range(1, 3):
        days.append((todayis['date'] + timedelta(days=i)).strftime("%d.%m.%Y")[:5])

    if todayis['date'] in fridays_before_public_holidays_2023:
        days.append((todayis['date'] + timedelta(days=3)).strftime("%d.%m.%Y")[:5])
        if todayis['date'] == datetime.date(2023, 5, 5):
            days.append((todayis['date'] + timedelta(days=4)).strftime("%d.%m.%Y")[:5])

# Если понедельник, проверяем на 2 дня назад
elif todayis['weekday'] == 0:
    Spcl_day = True
    for i in range(1, 3):
        days.append((todayis['date'] - timedelta(days=i)).strftime("%d.%m.%Y")[:5])
# Если вторник и это первый день после выходных проверяем на 3 дня назад
elif todayis['weekday'] == 1 and todayis['date'] in first_working_day_after_holidays_2023:
    Spcl_day = True
    for i in range(1, 4):
        days.append((todayis['date'] - timedelta(days=i)).strftime("%d.%m.%Y")[:5])
# Если это 10 мая проверяем на 4 дня назад
elif todayis['date'] == datetime.date(2023, 5, 10):
    Spcl_day = True
    for i in range(1, 5):
        days.append((todayis['date'] - timedelta(days=i)).strftime("%d.%m.%Y")[:5])
