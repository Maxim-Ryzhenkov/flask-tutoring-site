import os
import json

from config import Config
from app import app, db
from app.models import Tutor, Booking, Goal


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


def print_tutors_from_json(tutors_data):
    """ Напечатать id и имя для всех репетиторов из переменной tutors в JSON """
    for num, data in tutors_data.items():
        print(data)


def print_tutors_from_db():
    """ Напечатать id и имя для всех репетиторов из таблицы Tutors в базе данных """
    for item in Tutor.query.all():
        print(f'id: {item.id} - {item.name}')


def print_goals_from_json(goals_data):
    """ Напечатать все цели из переменной Goals в JSON """
    for num, data in goals_data.items():
        print(data)


def print_goals_from_db():
    """ Напечатать все цели из таблицы Goals в базе данных """
    for item in Goal.get_goals():
        print(item)


def transfer_goals_from_json_to_db(goals_data):
    """ Перенести записи о целях обучения из JSON в модель Goal """
    for num, data in goals_data.items():
        new_goal = Goal(goal=data)
        print(new_goal)
        db.session.add(new_goal)
    db.session.commit()


def transfer_tutors_from_json_to_db(tutors_data):
    """ Перенести записи о репетиторах из JSON в модель Tutor базы данных"""
    for num, data in tutors_data.items():
        new_tutor = Tutor.from_json(data)
        print(new_tutor)
        db.session.add(new_tutor)
    db.session.commit()


tutors_data = get_tutors_data()['teachers']
goals_data = get_tutors_data()['goals']

print_tutors_from_db()
