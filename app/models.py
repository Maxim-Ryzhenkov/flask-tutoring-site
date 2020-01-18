from time import time
from datetime import datetime

from app import app, db

tutors_goals = db.Table('tutors_goals',
                        db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),
                        db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id')))


class Tutor(db.Model):
    __tablename__ = "tutors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    about = db.Column(db.String(500))
    rating = db.Column(db.Float)
    price = db.Column(db.Integer)
    goals = db.relationship('Goal', secondary=tutors_goals)
    bookings = db.relationship('Booking', back_populates='tutor')
    timetable = db.Column(db.String(1000))

    def __init__(self, name, about, rating, price, timetable):
        self.name = name
        self.about = about
        self.rating = rating
        self.price = price
        self.timetable = timetable

    def __repr__(self):
        return f'<Tutor id {self.id} - {self.name}>'

    @property
    def avatar(self):
        return "https://i.pravatar.cc/300?img={}".format(24 + self.id)

    def add_goal(self, goal):
        if not self.has_goal(goal):
            self.goals.append(goal)

    def remove_goal(self, goal):
        if self.has_goal(goal):
            self.followed.remove(goal)

    def has_goal(self, goal):
        return goal in self.goals


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    text_en = db.Column(db.String(30), unique=True)
    text_ru = db.Column(db.String(30), unique=True)
    tutors = db.relationship('Tutor', secondary=tutors_goals)

    def __init__(self, text_ru, text_en):
        self.text_ru = text_ru
        self.text_en = text_en

    def __repr__(self):
        return f'<Goal: {self.text_en}: {self.text_ru}>'

    @staticmethod
    def get_goals():
        return [item.goal for item in Goal.query.all()]

    @staticmethod
    def add_new(text_ru, text_en):
        # TODO: Добавить проверку на уникальность
        goal = Goal(text_en=text_en, text_ru=text_ru)
        db.session.add(goal)
        db.session.commit()

    def delete(self, goal):
        raise NotImplemented


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_name = db.Column(db.String(64), index=True, unique=False)
    student_phone = db.Column(db.String(25), index=True, unique=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))
    tutor = db.relationship("Tutor", back_populates="bookings")
    date_time = db.Column(db.DateTime, index=True)
    closed = db.Column(db.Boolean, index=True, default=False)

    def __init__(self, student_name, student_phone, tutor_id, date_time):
        self.student_name = student_name
        self.student_phone = student_phone
        self.tutor_id = tutor_id
        self.date_time = date_time

    def __repr__(self):
        return '<Booking: tutor {} with {} - {}>'.format(
            Tutor.query.filter_by(id=self.tutor_id).first(),
            self.student_name, self.date_time)

    def is_accepted(self):
        pass

    def is_closed(self):
        pass

    def accept(self):
        pass

    def close(self):
        pass


class Pick(db.Model):
    __tablename__ = 'picks'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_name = db.Column(db.String(64), index=True, unique=False)
    student_phone = db.Column(db.String(25), index=True, unique=False)
    goal = db.Column(db.String(25), index=True, unique=False)
    hours = db.Column(db.Integer, index=True)
    closed = db.Column(db.Boolean, index=True, default=False)

    def __init__(self, student_name, student_phone, goal, hours):
        self.student_name = student_name
        self.student_phone = student_phone
        self.goal = goal
        self.hours = hours

    def __repr__(self):
        return f'<Request for search {self.id} - time: {self.timestamp} student: ' \
               f'"{self.student_name}", goal: "{self.goal}", hours: {self.hours}>'

    def is_closed(self):
        pass

    def close(self):
        pass
