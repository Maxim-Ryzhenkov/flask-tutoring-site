# -*- coding: utf-8 -*-
import os
import time
import json
import random
from datetime import datetime

from flask import flash, render_template, request, redirect, url_for
from app.models import Tutor, Goal, Pick, Booking

from app import app, db


@app.route('/')
@app.route('/index/')
def main():
    """ Главная страница сайта """
    tutors = random.sample(db.session.query(Tutor).all(), k=6)
    return render_template('index.html', tutors=tutors)


@app.route('/goals/<goal>/')
def goals(goal):
    """ Страница где показываются только репетиторы подходящие под цели обучения
     То есть если у них есть соответствующий тэг.
     """
    goal = db.session.query(Goal).filter(Goal.text_en == goal).first()
    return render_template("goal.html", goal=goal)


@app.route('/profile/<int:id>/')
def profile(id: int):
    """ Страница с индивидуальным профилем преподавателя """
    tutor = db.session.query(Tutor).filter(Tutor.id == id).first_or_404()
    schedule = json.loads(tutor.timetable)
    return render_template('profile.html', tutor=tutor, schedule=schedule)


@app.route('/pick/', methods=['GET', 'POST'])
def pick():
    """ Страница заявки на подбор репетитора """
    if request.method == 'POST':
        new_pick = Pick(student_name=request.form['user_name'], student_phone=request.form['phone'],
                        goal=request.form['goal'], hours=request.form['time'])
        db.session.add(new_pick)
        db.session.commit()
        goal = db.session.query(Goal).filter(Goal.text_en == request.form['goal']).first()
        return render_template('pick_confirmed.html', goal=goal, new_pick=new_pick)
    goals = db.session.query(Goal).all()
    return render_template("pick.html", goals=goals)


@app.route('/booking/<int:id>/', methods=['POST', 'GET'])
def booking(id):
    """ Страница формы бронирования занятий с репетитором """
    tutor = db.session.query(Tutor).filter(Tutor.id == id).first_or_404()
    booking_day = request.args.get("d")
    booking_hour = request.args.get("h")
    days = {"mon": "понедельник", "tue": "вторник", "wed": "среда", "thu": "четверг", "fri": "пятница",
            "sat": "суббота", "sun": "воскресенье"}

    if request.method == 'POST':
        new_booking = Booking(student_name=request.form['user_name'], student_phone=request.form['phone_number'],
                              tutor_id=tutor.id, date_time=datetime.utcnow())
        db.session.add(new_booking)
        db.session.commit()
        return render_template('booking_confirmed.html', booking=new_booking)
    return render_template('booking.html', tutor=tutor, booking_hour=booking_hour, booking_day=days[booking_day])


@app.route('/message/<int:id>/', methods=["GET", "POST"])
def message(id):
    """ Страница формы бронирования занятий с репетитором """
    tutor = db.session.query(Tutor).filter(Tutor.id == id).first_or_404()
    if request.method == "POST":
        return render_template('message_confirmed.html')
    return render_template('message.html', tutor=tutor)
