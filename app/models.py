from time import time
from datetime import datetime

from app import app, db


# tutors_goals_association = db.Table('tutors_goals',
#                                     db.Column('tutor_id', db.Integer, db.ForeignKey('tutor.id')),
#                                     db.Column('goal_id', db.Integer, db.ForeignKey('goal.id')))


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    about = db.Column(db.String(500))
    rating = db.Column(db.Float)
    price = db.Column(db.Integer)

    #  goals = db.relationship('Goal', secondary=tutors_goals_association, back_populates='tutors')

    def __repr__(self):
        return '<Tutor {}>'.format(self.name)

    def avatar(self):
        return "https://i.pravatar.cc/300?img={}".format(24 + self.id)

    def add_goal(self, goal):
        pass

    def remove_goal(self, goal):
        pass

    def get_goals(self):
        pass

    @staticmethod
    def from_json(source):
        return Tutor(name=source['name'], about=source['about'], rating=source['rating'], price=source['price'])


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(30), index=True, unique=True)

    # tutors = db.relationship('Tutor', secondary=tutors_goals_association, back_populates='users')

    def __repr__(self):
        return '<Goal: {}>'.format(self.goal)

    @staticmethod
    def get_goals():
        return [item.goal for item in Goal.query.all()]

    def new_goal(self, goal):
        pass

    def delete_goal(self, goal):
        pass


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_name = db.Column(db.String(64), index=True, unique=True)
    student_phone = db.Column(db.String(25), index=True, unique=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    date_time = db.Column(db.DateTime, index=True)
    closed = db.Column(db.Boolean, index=True, default=False)

    def __repr__(self):
        return '<Booking: tutor {} with {} - {}>'.format(
            Tutor.query.filter_by(id=self.tutor_id).first(),
            self.student_name, self.date_time)


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    student_name = db.Column(db.String(64), index=True, unique=True)
    student_phone = db.Column(db.String(25), index=True, unique=True)
    goal = db.Column(db.String(25), index=True, unique=True)
    hours = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Request for search: student - "{}", main goal - "{}", hours per week{}>'.format(
            self.student_name, self.goal, self.hours)
