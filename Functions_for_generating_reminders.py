from Lead_preferences import departments_and_leads, lead_preferences, student_group, departments_with_teams, \
    teams_with_students, departments_with_several_people_to_notify

import pandas as pd
import datetime
from enum import Enum


class When(Enum):
    not_defined = ''
    today = 'Сегодня'
    future = 'На выходных будет'
    past = 'На выходных был'


class Sotrudnik:
    def __init__(self):
        self.__name = ''
        self.__dep = ''
        self.__age = 0
        self.__birthday = ''
        self.__leads = []

    # ИМЯ
    # геттер
    @property
    def name(self):
        return self.__name

    # сеттер
    @name.setter
    def name(self, name):
        self.__name = name

    # ДЕПАРТАМЕНТ
    # геттер
    @property
    def dep(self):
        return self.__dep

    # сеттер
    @dep.setter
    def dep(self, dep):
        self.__dep = dep

    # ВОЗРАСТ
    # геттер
    @property
    def age(self):
        return self.__age

    # сеттер
    @age.setter
    def age(self, age):
        self.__age = age

    # ДР
    # геттер
    @property
    def birthday(self):
        return self.__birthday

    # сеттер
    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    # Лиды сотрудника
    # геттер
    @property
    def list_of_leads(self):
        if self.__dep == student_group:
            for team in teams_with_students:
                if self.__name in team[0]:
                    self.__leads += team[1]
                    break
        else:
            self.__leads = [departments_and_leads[self.__dep]]
            for dep_with_teams in departments_with_teams:
                if self.__dep == dep_with_teams:
                    for team in departments_with_teams[dep_with_teams]:
                        if self.__name in team[0]:
                            self.__leads += team[1]
                            break
            if self.__dep in departments_with_several_people_to_notify:
                self.__leads += departments_with_several_people_to_notify[self.__dep]
        return self.__leads


class BirthdayReminder:
    def __init__(self, today_date, sotrudnik, lead_name):

        self.today_date = today_date
        self.sotrudnik = sotrudnik
        self.lead_name = lead_name
        self.when = When.not_defined

        if sotrudnik.birthday == today_date:
            self.when = When.today
        elif sotrudnik.birthday > today_date:
            self.when = When.future
        else:
            self.when = When.past


class Lead:
    def __init__(self, name):
        self.name = name
        self.time_preference = lead_preferences[name][0]
        self.show_age_preference = lead_preferences[name][1]

        self.birthday_reminders_for_today = []

    def add_b_reminder_if_lead_needs_it(self, today_date, day_type, sotrudnik):
        if not day_type or \
            (sotrudnik.birthday >= today_date and self.time_preference.name in ['before', 'unknown']) or \
                (sotrudnik.birthday <= today_date and self.time_preference.name == 'after'):
            self.birthday_reminders_for_today.append(BirthdayReminder(today_date, sotrudnik, self.name))


class ReminderMessage:
    greeting = 'Доброе утро!'
    ending = 'Хорошего дня!'
    spcl_message = 'Я с недавнего времени занимаюсь рассылкой руководителям напоминаний в чате о ДР их сотрудников. ' \
                   'Вы есть в списке руководителей, которые когда-то подписывались на такие напминания. ' \
                   'Для вас это все еще актуально? Если да, то просьба пройти минутный опрос: <ccылка>. ' \
                   'Рассылка будет в таком формате: '

    def __init__(self, lead_name: str, birthday_reminders: list):
        self.__lead_name = lead_name
        self.__birthday_reminders = birthday_reminders

    def form_sentences(self):
        sentences = {}
        for reminder in self.__birthday_reminders:
            if reminder.when not in sentences:
                sentences[reminder.when] = [reminder.sotrudnik]
            else:
                sentences[reminder.when].append(reminder.sotrudnik)
        return sentences

    def generate_main_text(self):
        show_age = lead_preferences[self.__lead_name][1]
        sentences_dict = self.form_sentences()
        main_text = ''
        for adj in sentences_dict:
            main_text = f'{adj.value} ДР у '
            for sotrudnik in sentences_dict[adj]:
                if not show_age:
                    main_text += sotrudnik.name
                else:
                    main_text += f'{sotrudnik.name} ({sotrudnik.age} лет)'
        return main_text

    def __str__(self):
        if lead_preferences[self.__lead_name][1] == 'dk':
            return '\n'.join([self.__lead_name,
                              f'{ReminderMessage.greeting} {ReminderMessage.spcl_message}{self.generate_main_text()}. '
                              f'{ReminderMessage.ending}'])
        else:
            return '\n'.join([self.__lead_name,
                              f'{ReminderMessage.greeting} {self.generate_main_text()}. {ReminderMessage.ending}'])


# ----------------add_to_dict-----------------
# Функция проверяет, есть ли key в словаре и корректно пополняет словарь

def add_to_dict(dictionary_name, key, value):
    if key not in dictionary_name:
        dictionary_name[key] = [value]
    else:
        dictionary_name[key].append(value)



def add_lead_to_reminders_dict(dictionary_name, key_lead, value):
    if key_lead not in dictionary_name:
        dictionary_name[key_lead] = [value]
    else:
        # Если у лида больше одного сотрудника празднуют ДР и этому лиду нужно послать напоминание пройти опрос
        if len(value) == 3:
            value.pop(0)
        dictionary_name[key_lead].append(value)


# -----------------------mssg_text_func---------------------
# На вход подаются 1) сегодняшняя дата, 2) имя\фамилия сотрудника (без отчества), 3) День, 4) Предочтение руковдителя
# по возрасту, 5) Возраст. Определяем наречие (если 3)День совпадает с 0)сегодняшней датой, то "сегодня", если нет, то
# "на выходных"). Если наречие "на выходных", то определяем глагол (если 3)День больше 0)сегодняшней даты, то "будет",
# если меньше, то "был"). Смотрим на 4)предпочтения руководителя (если 'yes', присваеваем переменной age значение из
# колонки str(Возраст) в скобках, если 'no', ''). На выходе список ['наречие + глагол', '{2)имя сотрудника + age']

def mssg_text_func(today_date, ns, birthday, lead_need_age, age):
    if birthday == today_date:
        adj = 'Сегодня'
        verb = ''
    else:
        adj = 'На выходных '
        if birthday > today_date:
            verb = 'будет'
        else:
            verb = ' был'
    age = f' ({str(age)} лет)'
    if not lead_need_age:
        age = ''
    elif lead_need_age == 'dk':
        Spcl_message = 'Напоминание'

        return [Spcl_message, adj + verb, ns + age]

    return [adj + verb, ns + age]


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

def generating_reminder_mssgs_func(what_date_is_it_today: dict, day_type: bool, prepared_table: pd.DataFrame):
    today_reminders_dict = {}
    Shaforost_team = []

    leads_with_mssgs = {}

    # Для каждой строки в табличке:
    for index, row in prepared_table.iterrows():
        employee = Sotrudnik()
        employee.dep = row[prepared_table.columns.get_loc('Код')]
        employee.name = row[prepared_table.columns.get_loc('Фамилия имя отчество сотрудника')]
        employee.birthday = row[prepared_table.columns.get_loc('День')]
        employee.age = row[prepared_table.columns.get_loc('Возраст')]
        # --------------Составляем список лидов каждого сотрудника -------------------
        # Ловим сотрудников Шафороста
        if employee.dep == '762':
            Shaforost_team.append([employee.name, employee.birthday])

        for each_lead in employee.list_of_leads:
            if each_lead not in leads_with_mssgs:
                leads_with_mssgs[each_lead] = Lead(each_lead)
            leads_with_mssgs[each_lead].add_b_reminder_if_lead_needs_it(what_date_is_it_today['date'], day_type, employee)

        # ---------------Решаем, кому из списка лидов сотрудника нужно напоминать о его ДР --------
        # Тех лидов, кому надо напоминать, добавляем в словарь today_reminders_dict вместе с текстом напоминания
        if not day_type:  # то напоминаем всем лидам
            for each_lead in employee.list_of_leads:
                reminder_text = mssg_text_func(what_date_is_it_today['date'],
                                               employee.name,
                                               employee.birthday,
                                               lead_preferences[each_lead][1],
                                               employee.age)
                add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)
        else:  # нужно смотреть предпочтения каждого лида
            for each_lead in employee.list_of_leads:
                if employee.birthday >= what_date_is_it_today['date'] and lead_preferences[each_lead][0].name in \
                        ['before',
                         'unknown']:  # добавляем each_lead в словарь today_reminders_dict вместе с текстом напоминания

                    reminder_text = mssg_text_func(what_date_is_it_today['date'],
                                                   employee.name,
                                                   employee.birthday,
                                                   lead_preferences[each_lead][1],
                                                   employee.age)
                    add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)
                if employee.birthday <= what_date_is_it_today['date'] and lead_preferences[each_lead][
                    0].name == 'after':  # добавляем each_lead в словарь today_reminders_dict вместе с текстом напоминания
                    reminder_text = mssg_text_func(what_date_is_it_today['date'],
                                                   employee.name,
                                                   employee.birthday,
                                                   lead_preferences[each_lead][1],
                                                   employee.age)
                    add_lead_to_reminders_dict(today_reminders_dict, each_lead, reminder_text)

    print('\n', today_reminders_dict, '\n', sep='')

    for lead in leads_with_mssgs:
        if leads_with_mssgs[lead].birthday_reminders_for_today:
            print(ReminderMessage(lead, leads_with_mssgs[lead].birthday_reminders_for_today))
    print('\n')
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
