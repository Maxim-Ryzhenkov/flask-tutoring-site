import os
import json
from datetime import datetime

from config import Config
from app import app, db
from app.models import Tutor, Booking, Goal, Pick


def get_data(file_name: str):
    """ Прочитать данные из указанного файла json и вернуть их как словарь
    Args:
        file_name: полный путь к файлу .json
    Returns:
        data: dict - содержимое json файла в виде словаря
    """
    if not os.path.exists(file_name):
        raise OSError(f"Файл не найден: {file_name}")
    with open(file_name, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    return data


def get_tutors_data():
    """ Прочитать данные о репетиторах из файла data.json и вернуть как словарь """
    tutors_json = os.path.abspath(os.path.join(Config.ROOT_DIR, 'data.json'))
    return get_data(tutors_json)


def print_tutors_from_json():
    """ Напечатать id и имя для всех репетиторов из переменной tutors в JSON """
    tutors_data = get_tutors_data()['teachers']
    for num, data in tutors_data.items():
        print(data)


def print_goals_from_json():
    goals_data = get_tutors_data()['goals']
    """ Напечатать все цели из переменной Goals в JSON """
    for num, data in goals_data.items():
        print(data)


def transfer_goals_from_json_to_db():
    """ Перенести записи о целях обучения из JSON в модель Goal """
    goals_data = get_tutors_data()['goals']
    for text_en, text_ru in goals_data.items():
        new_goal = Goal(text_en=text_en, text_ru=text_ru)
        print(new_goal)
        db.session.add(new_goal)
    db.session.commit()


def transfer_tutors_from_json_to_db():
    """ Перенести записи о репетиторах из JSON в модель Tutor базы данных"""
    tutors_data = get_tutors_data()['teachers']

    for tutor_id, tutor_data in tutors_data.items():
        new_tutor = Tutor(name=tutor_data['name'],
                          about=tutor_data['about'],
                          rating=tutor_data['rating'],
                          price=tutor_data['price'],
                          timetable=json.dumps(tutor_data['free']))
        for tutors_goal in tutor_data['goals']:
            goal = db.session.query(Goal).filter(Goal.text_en == tutors_goal).first()
            new_tutor.goals.append(goal)
        db.session.add(new_tutor)
    db.session.commit()


def print_db_table(model):
    """ напечатать все зхаписи в таблице с указанной моделью данных"""
    for record in db.session.query(model).all():
        print(record)


def clear_db_table(model):
    """ удалить все зхаписи в таблице с указанной моделью данных"""
    for record in db.session.query(model).all():
        db.session.delete(record)
    db.session.commit()


# Для обновления базы предварительно надо удалить файл app.db и папку migrations
# Затем активировать venv и набрать в терминале
# 1. flask db init
# 2. flask db migrate
# 3. flask db upgrade

# Затем раскомментировать и запустить. После запуска снова закомментировать
transfer_goals_from_json_to_db()
#transfer_tutors_from_json_to_db()

# Убедиться что данные перенеслись корректно можно посмотрев вывод на печать
# вместо model надо передать Tutor, Goal, Pick или Booking
# clear_db_table(Pick)
# print_db_table(Pick)

#
# tutors_data = get_tutors_data()['teachers']
# for tutor_id, tutor_info in tutors_data.items():
#     tutor = db.session.query(Tutor).get(int(tutor_id))
#     tutor.timetable = json.dumps(tutor_info['free'])
#     db.session.add(tutor)
# # db.session.commit()
# item = db.session.query(Goal).get(1)
# print(item.text_ru)
