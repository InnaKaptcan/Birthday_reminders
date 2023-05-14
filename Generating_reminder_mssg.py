from Lead_preferences import departents_and_leads, lead_preferences,\
    Alenikov_team, Dmitriev_team, Nuraliev_team, Damie_team, Derut_team, Lakutin_team, Lebovich_team,\
    birthdays_not_in_1C_table2023
from Days_of_interest import todayis, todays_file_name, Spcl_day
from Preparing_table import birthdays7dep

import os
import warnings
warnings.filterwarnings("ignore")


# ----------------add_lead_to_reminders_dict-----------------
# Функция проверяет, есть ли lead в словаре today_reminders_dict и корректно пополняет словарь


def add_lead_to_reminders_dict(dictionary, key_lead, value_message):
    if key_lead not in dictionary:
        dictionary[key_lead] = [value_message]
    else:
        # Если у лида больше одного сотрудника празднуют ДР и этому лиду нужно послать напоминание пройти опрос
        if len(value_message) == 3:
            value_message.pop(0)
        dictionary[key_lead].append(value_message)


# -----------------------mssg_text_func---------------------
# На вход подаются 1) сегодняшняя дата, 2) имя\фамилия сотрудника (без отчества), 3) День, 4) Предочтение руковдителя
# по возрасту, 5) Возраст. Определяем наречие (если 3)День совпадает с 0)сегодняшней датой, то "сегодня", если нет, то
# "на выходных"). Если наречие "на выходных", то определяем глагол (если 3)День больше 0)сегодняшней даты, то "будет",
# если меньше, то "был"). Смотрим на 4)предпочтения руководителя (если 'yes', присваеваем переменной age значение из
# колонки str(Возраст) в скобках, если 'no', ''). На выходе список ['наречие + глагол', '{2)имя сотрудника + age']

def mssg_text_func(today_date, NS, birthDay, lead_need_age, age):
    if birthDay == today_date:
        adj = 'Сегодня'
        verb = ''
    else:
        adj = 'На выходных '
        if birthDay > today_date:
            verb = 'будет'
        else:
            verb = ' был'
    if lead_need_age == 'yes':
        age = f' ({str(age)} лет)'
    elif lead_need_age == 'no':
        age = ''
    elif lead_need_age == 'dk':
        age = f' ({str(age)} лет)'
        Spcl_message = 'Напоминание'

        return [Spcl_message, adj + verb, NS + age]

    return [adj + verb, NS + age]


weekday_names = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}


# Для каждой строчки таблицы birthdays7dep:
## Смотрим на код, определяем руководителя/ей
### Если сегодня обычный день, нужно сформировать текст напоминания для каждого руководителя каждого сотрудника.
### Создаем словарь, где имени каждого руководителя соответствует пустой список.
### Пополняем этот список результатом функции, которая формирует напоминание.

### Если сегодня "особый день", проверяем предпочтения для каждого руководителя
### Если у руководителя предпочтение before и День больше или равен сегоняшнему числу, то добавляем этого руководителя в словарь и
### пополняем этот список результатом функции, которая формирует напоминание по этому сотруднику, этому руководителю.
### То же самое, если after и День меньше или равен сегоняшнему числу.

# После того, как мы определили, нужно сегодня напоминать про ДР этого сотрудника этому руководителю, применяеем функцию, которая
# формирует текст напоминания.


today_reminders_dict = {}
Shaforost_team = []

# Для каждой строки в табличке:
for index, row in birthdays7dep.iterrows():
    list_of_his_leads = []
    his_dep = row[6]
    his_name = row[1]
    his_birthday = row[3]
    his_age = row[4]

    # Ловим сотрудников Шафороста
    if his_dep == '762':
        Shaforost_team.append([his_name, his_birthday])
    # --------------Составляем список лидов сотрудника -------------------

    list_of_his_leads = [departents_and_leads[his_dep]]
    if his_dep == '77':
        if his_name in Dmitriev_team:
            list_of_his_leads.append('Дмитриев Владислав')
        elif his_name in Nuraliev_team:
            list_of_his_leads.append('Нуралиев Антон')
        elif his_name in Damie_team:
            list_of_his_leads.append('Дамье Геннадий')
        elif his_name in Derut_team:
            list_of_his_leads.append('Дерут Одей')
        elif his_name in Lakutin_team:
            list_of_his_leads.append('Лакутин Алексей')
        elif his_name in Lebovich_team:
            list_of_his_leads.append('Лейбович Максим')
    elif his_dep == '70':
        if his_name in Dmitriev_team:
            list_of_his_leads.append('Дмитриев Владислав')
        elif his_name in Alenikov_team:
            list_of_his_leads.append('Алейников Роман')

        # ---------------Решаем, кому из списка лидов нужно напоминать о ДР этого сотрудника --------
        # Тех лидов, кому надо напоминать, добавляем в словарь today_reminders_dict вместе с текстом напоминания
    if not Spcl_day:  # то напоминаем всем лидам
        for each_lead in list_of_his_leads:
            if each_lead not in today_reminders_dict:
                reminder_text = mssg_text_func(todayis['date'].strftime("%d.%m"),
                                               his_name,
                                               his_birthday,
                                               lead_preferences[each_lead][1],
                                               his_age)
                add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)
    else:  # нужно смотреть предпочтения каждого лида
        for each_lead in list_of_his_leads:
            if his_birthday >= todayis['date'].strftime("%d.%m") and lead_preferences[each_lead][0] in ['before',
                                                                                                        'dk']:  # добавляем each_lead в словарь today_reminders_dict вместе с текстом напоминания
                reminder_text = mssg_text_func(todayis['date'].strftime("%d.%m"),
                                               his_name,
                                               his_birthday,
                                               lead_preferences[each_lead][1],
                                               his_age)
                add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)
            if his_birthday <= todayis['date'].strftime("%d.%m") and lead_preferences[each_lead][0] == 'after':  # добавляем each_lead в словарь today_reminders_dict вместе с текстом напоминания
                reminder_text = mssg_text_func(todayis['date'].strftime("%d.%m"),
                                               his_name,
                                               his_birthday,
                                               lead_preferences[each_lead][1],
                                               his_age)
                add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)

print(weekday_names[todayis['weekday']], todayis['date'], '\n')
for lead in today_reminders_dict:
    print(lead)
    text_body = 'Доброе утро! '
    # Проверяем нужно ли посылать лиду напоминание пройти опрос
    if len(today_reminders_dict[lead][0]) == 3:
        today_reminders_dict[lead][0].pop(0)
        text_body += 'Я с недавнего времени занимаюсь рассылкой руководителям напоминаний в чате о ДР их сотрудников. ' \
                     'Вы есть в списке руководителей, которые когда-то подписывались на такие напминания. ' \
                     'Для вас это все еще актуально? Если да, то просьба пройти минутный опрос: <ccылка>. ' \
                     'Рассылка будет в таком формате: '
    if len(today_reminders_dict[lead]) > 1:
        text_reminders_dict = {}  # словарь, составленный по принципу {'наречие + глагол': именинники каждого лида, у которых сообщение начинается с одинаковых
        # наречий в одном списке
        for empl_info in today_reminders_dict[lead]:
            if empl_info[0] not in text_reminders_dict:
                text_reminders_dict[empl_info[0]] = [empl_info[1]]
            else:
                text_reminders_dict[empl_info[0]].append(empl_info[1])
        # Составляем из словаря text_reminders_dict текст напоминания лиду text_body
        for adj in list(text_reminders_dict.keys()):
            text_for_adj = f'{adj} ДР у '
            for empl_name in text_reminders_dict[adj]:
                text_for_adj += empl_name
            text_body += text_for_adj

    else:
        text_body += f'{today_reminders_dict[lead][0][0]} ДР у {today_reminders_dict[lead][0][1]}'
    text_body += '. Хорошего дня!'
    print(text_body)
print('\n')
for person in Shaforost_team:
    print(f'У сотрудника Шафороста {person[0]} ДР {person[1]}')


# Удалим таблички из загрузок
# os.remove(path=todays_file_name + '.xls')
os.remove(path=todays_file_name + '.xlsx')
