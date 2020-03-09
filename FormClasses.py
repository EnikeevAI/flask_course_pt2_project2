from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, PasswordField, RadioField, StringField, SubmitField
from wtforms.validators import InputRequired


client_free_time = {"time1": "1-2", "time2": "3-5", "time3": "5-7", "time4": "7-10"}


class BookingForm(FlaskForm):
    clientWeekday = HiddenField('clientWeekday')
    clientTime = HiddenField('clientTime')
    clientTeacher = HiddenField('clientTeacher')
    clientName = StringField('Вас зовут', [InputRequired(message='Необходимо указать Ваше имя')])
    clientPhone = StringField('Ваш телефон', [InputRequired(message='Необходимо указать Ваш телефон для связи')])
    submit = SubmitField('Записаться на пробный урок')

class RequestForm(FlaskForm):
    clientName = StringField('Вас зовут', [InputRequired(message='Необходимо указать Ваше имя')])
    clientPhone = StringField('Ваш телефон', [InputRequired(message='Необходимо указать Ваш телефон для связи')])
    clientGoals = RadioField('clientGoals', choices=[("travel", "⛱Для путешествий"), ("study", "🏫 Для учёбы"),
                                                     ("work", "🏢 Для работы"), ("relocate", "🚜 Для переезда")])
    clientFreeTime = RadioField('clientFreeTime', choices=[("1-2", "1-2"), ("3-5", "3-5"),
                                                           ("5-7", "5-7"), ("7-10", "7-10")])
    submit = SubmitField('Найдите мне преподавателя')