import os
import time
import json
import logging
from flask import Flask, render_template, request, redirect, url_for

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app_dir = os.path.split(os.path.realpath(__file__))[0]
app_time_format = "%d.%b.%Y - %X"


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


def put_data(file_name: str, data: dict):
    """ Записать данные в файл json. !!! Файл будет перезаписан!
    Args:
        file_name: полный путь к файлу .json
        data: слдоварь для записи в json
    """
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def add_booking(booking_data: dict):
    """ Добавить новую запись о бронировании в файле booking.json
        - Если файл не существует, он будет создан и в него будет добавлен ключ "bookings: {}"
        - Если файл уже есть, то он будет прочитан в словарь.
        - Новая запись будет добавлена в словарь
        - После этого словарь будет записан обратно в файл booking.json.
    """
    booking_json = os.path.abspath(os.path.join(app_dir, 'booking.json'))
    if not os.path.exists(booking_json):
        put_data(booking_json, {'bookings': {}})
    data = get_data(booking_json)
    data['bookings'].update(booking_data)
    put_data(booking_json, data)


def add_tutor_request(request_data: dict):
    """ Добавить новую запись о заявке на подбор репетитора в файле request_tutor.json
        - Если файл не существует, он будет создан и в него будет добавлен ключ "requests: {}"
        - Если файл уже есть, то он будет прочитан в словарь.
        - Новая запись будет добавлена в словарь
        - После этого словарь будет записан обратно в файл request_tutor.json.
    """
    request_tutor_json = os.path.abspath(os.path.join(app_dir, 'request_tutor.json'))
    if not os.path.exists(request_tutor_json):
        put_data(request_tutor_json, {'requests': {}})
    data = get_data(request_tutor_json)
    data['requests'].update(request_data)
    put_data(request_tutor_json, data)


def get_tutors_data():
    """ Прочитать данные о репетиторах из файла data.json и вернуть как словарь """
    tutors_json = os.path.abspath(os.path.join(app_dir, 'data.json'))
    return get_data(tutors_json)


@app.route('/')
def main():
    """ Главная страница сайта """
    teachers = get_tutors_data()['teachers']
    return render_template('index.html', teachers=teachers)


@app.route('/goals/<goal>/')
def goals(goal):
    """ Страница где показываются только репетиторы подходящие под цели обучения
     То есть если у них есть соответствующий тэг.
     """
    teachers = get_tutors_data()['teachers']
    teachers = {k: v for k, v in teachers.items() if goal in v['goals']}
    goals_list = {"travel": {"text": "для путешествий", "icon": "⛱"},
                  "study": {"text": "для школы", "icon": "🏫"},
                  "work": {"text": "для работы", "icon": "🏢"},
                  "relocate": {"text": "для переезда", "icon": "🚜"}}
    return render_template("goal.html", teachers=teachers, goal=goals_list[goal])


@app.route('/profile/<int:id>/')
def profile(id: int):
    """ Страница с индивидуальным профилем преподавателя """
    teachers = get_tutors_data()['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    return render_template('profile.html', teacher=teachers[str(id)], teacher_id=str(id))


@app.route('/pick/', methods=['GET', 'POST'])
def pick():
    """ Страница заявки на подбор репетитора """
    if request.method == 'POST':
        request_time = time.strftime(app_time_format)
        request_data = {"user name": request.form['user_name'],
                        "phone": request.form['phone'],
                        "time": request.form['time'],
                        "goal": request.form['goal']}
        add_tutor_request({request_time: request_data})
        return render_template('pick_confirmed.html', data=request_data)
    return render_template("pick.html")


@app.route('/booking/<int:id>/', methods=['POST', 'GET'])
def booking(id):
    """ Страница формы бронирования занятий с репетитором """
    teachers = get_tutors_data()['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    teacher = teachers[str(id)]
    booking_day = request.args.get("d")
    booking_time = request.args.get("h")
    days = {"mon": "понедельник", "tue": "вторник", "wed": "среда", "thu": "четверг", "fri": "пятница", "sat": "суббота", "sun": "воскресенье"}

    if request.method == 'POST':
        booking_time = time.strftime(app_time_format)
        booking_data = {"user name": request.form['user_name'],
                        "phone": request.form['phone_number'],
                        "day": days[booking_day],
                        "time": booking_time,
                        "tutor": {"id": id, "name": teacher['name']}}
        add_booking({booking_time: booking_data})
        return render_template('booking_confirmed.html', booking_data=booking_data)
    return render_template('booking.html', teacher=teacher, booking_time=booking_time, booking_day=days[booking_day])


@app.route('/message/<int:id>/', methods=["GET", "POST"])
def message(id):
    """ Страница формы бронирования занятий с репетитором """
    teachers = get_tutors_data()['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    if request.method == "POST":
        return render_template('message_confirmed.html')
    return render_template('message.html', teacher=teachers[str(id)])


@app.errorhandler(404)
def not_found(e):
    return render_template('page404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('page500.html')


if __name__ == '__main__':
    app.run(debug=True)
