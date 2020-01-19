# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime

from flask import render_template, request, url_for
from app import app, db
from app.forms import BookingForm, PickForm
from app.models import Tutor, Goal, Pick, Booking


@app.route('/')
@app.route('/index/')
def main():
    """ Главная страница сайта """
    tutors = random.sample(Tutor.query.all(), k=6)
    return render_template('index.html', tutors=tutors)


@app.route('/goals/<goal>/')
def goals(goal):
    """ Страница где показываются только репетиторы подходящие под цели обучения
     То есть если у них есть соответствующий тэг.
     """
    goal = Goal.query.filter(Goal.text_en == goal).first()
    return render_template("goal.html", goal=goal)


@app.route('/profile/<int:id>/')
def profile(id: int):
    """ Страница с индивидуальным профилем преподавателя """
    tutor = Tutor.query.get_or_404(id)
    schedule = json.loads(tutor.timetable)
    return render_template('profile.html', tutor=tutor, schedule=schedule)


@app.route('/pick/', methods=['GET', 'POST'])
def pick():
    """ Страница заявки на подбор репетитора """
    form = PickForm()
    if request.method == 'POST':
        new_pick = Pick(student_name=form.student_name.data,
                        student_phone=form.phone_number.data,
                        goal=form.goal.data, hours=form.time_available.data)
        db.session.add(new_pick)
        db.session.commit()
        goal = Goal.query.filter(Goal.text_en == new_pick.goal).first()
        return render_template('pick_confirmed.html', goal=goal, new_pick=new_pick)
    goals = db.session.query(Goal).all()
    return render_template("pick.html", goals=goals, form=form)


@app.route('/booking/<int:id>/', methods=['POST', 'GET'])
def booking(id):
    """ Страница формы бронирования занятий с репетитором """

    tutor = Tutor.query.get_or_404(id)
    days = {"mon": "понедельник", "tue": "вторник", "wed": "среда", "thu": "четверг", "fri": "пятница",
            "sat": "суббота", "sun": "воскресенье"}
    booking_day = days[request.args.get("d")]
    booking_hour = request.args.get("h")
    form = BookingForm()

    if request.method == 'POST':
        new_booking = Booking(student_name=form.student_name.data,
                              student_phone=form.phone_number.data,
                              tutor_id=tutor.id, date_time=datetime.utcnow())
        db.session.add(new_booking)
        db.session.commit()
        return render_template('booking_confirmed.html', booking=new_booking)
    return render_template('booking.html', tutor=tutor, booking_hour=booking_hour, booking_day=booking_day, form=form)


@app.route('/message/<int:id>/', methods=["GET", "POST"])
def message(id):
    """ Страница формы бронирования занятий с репетитором """
    tutor = Tutor.query.get_or_404(id)
    if request.method == "POST":
        return render_template('message_confirmed.html')
    return render_template('message.html', tutor=tutor)
