from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, HiddenField


class BookingForm(FlaskForm):
    clientWeekday = HiddenField('clientWeekday')
    clientTime = HiddenField('clientTime')
    clientTeacher = HiddenField('clientTeacher')
    clientName = StringField('clientName')
    clientPhone = StringField('clientPhone')
    submit = SubmitField('Записаться на пробный урок')