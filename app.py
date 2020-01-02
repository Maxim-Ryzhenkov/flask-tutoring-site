import os
import time
import json
import logging
from flask import Flask, render_template, request, redirect, url_for


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app_dir = os.path.split(os.path.realpath(__file__))[0]


def get_data(file_name: str):
    """ Чтение данных из файла json
    Args:
        file_name: относительный путь к файлу .json
    """
    file_name = os.path.abspath(os.path.join(app_dir, file_name))
    if not os.path.exists(file_name):
        raise OSError
    logging.debug(f"Файл с данными найден: {file_name}")
    with open(file_name, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    return data


def add_data_to(file_name: str, new_data: dict):
    """ Добавление данных в файла json
    Args:
        file_name: относительный путь к файлу .json
        new_data: слдоварь для добавления в json
    """
    file_name = os.path.abspath(os.path.join(app_dir, file_name))
    data: dict = {}
    if os.path.exists(file_name) and os.stat(file_name).st_size != 0:
        data = get_data(file_name)
    data.update(new_data)
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


@app.route('/')
def main():
    teachers = get_data('data.json')['teachers']
    return render_template('index.html', teachers=teachers)


@app.route('/goals/<goal>')
def goals(goal):
    """ Страница где показываются только репетиторы подходящие под цели обучения
     То есть если у них есть соответствующий тэг.
     """
    return render_template('goal.html')


@app.route('/profiles/<int:id>')
def profiles(id):
    """ Страница с индивидуальным профилем преподавателя """
    teachers = get_data('data.json')['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    return render_template('profile.html', teacher=teachers[str(id)])


@app.route('/search')
def search():
    """ Страница поиска """
    return render_template('search.html')


@app.route('/request')
def request():
    """ Страница заявки на подбор репетитора """
    return render_template("pick.html")


@app.route('/booking/<int:id>', methods=['POST', 'GET'])
def booking(id):
    """ Страница формы бронирования занятий с репетитором """
  #  form = BookingForm()
    teachers = get_data('data.json')['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    teacher = teachers[str(id)]

    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        phone = request.form.get('password')
        booking_info = {"time": time.localtime(),
                        "user name": username,
                        "phone": phone,
                        "teacher": {"id": id, "name": teacher['name']}}
        add_data_to('booking.json', booking_info)
    return render_template('booking.html', teacher=teacher)


@app.route('/sent')
def sent():
    """ Страница подтверждения бронирования """
    return render_template("sent.html")

@app.route('/message/<int:id>')
def message(id):
    """ Страница формы бронирования занятий с репетитором """
    teachers = get_data('data.json')['teachers']
    if str(id) not in teachers.keys():
        return render_template('page404.html')
    print(teachers)
    return render_template('message.html', teacher=teachers[str(id)])


@app.errorhandler(404)
def not_found(e):
    return render_template('page404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('page500.html')


if __name__ == '__main__':
    app.run(debug=True)

    # data = get_data('data.json')
    # teachers = data['teachers']
    # print(teachers['1'])