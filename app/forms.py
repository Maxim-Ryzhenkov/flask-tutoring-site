from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Goal


class BookingForm(FlaskForm):
    student_name = StringField('Вас зовут', validators=[DataRequired(), Length(min=2, max=32)])
    phone_number = StringField('Телефон для связи', validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField('Записаться на пробный урок')


class PickForm(FlaskForm):
    student_name = StringField('Вас зовут', validators=[DataRequired(), Length(min=2, max=32)])
    phone_number = StringField('Телефон для связи', validators=[DataRequired(), Length(min=8, max=16)])
    goal = RadioField('Какая цель занятий?', choices=[('travel', 'Для путешествий'), ('study', 'Для учебы'),
                                                      ('work', 'Для работы'), ('relocate', 'Для переезда')])
    time_available = RadioField('Сколько времени есть?', choices=[('1-2', '1-2 часа в неделю'),
                                                                  ('3-5', '3-5 часов в неделю'),
                                                                  ('5-7', '5-7 часов в неделю'),
                                                                  ('7-10', '7-10 часов в неделю')])

    submit = SubmitField('Найдите мне преподавателя')
