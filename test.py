import os
import json
from datetime import datetime
#
# from config import Config
# from app import app, db
# from app.models import Tutor, Booking, Goal, Pick


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

file_path = r'C:\Projects\Flask_learning\flask-tutoring-site\data.json'

d = get_data(file_path)['teachers']
print(len(d))
