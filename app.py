import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, HiddenField
import json
from data import week, client_free_time
from db_create_script import Booking, Goal, Request, Teacher
from FormClasses import BookingForm



app = Flask(__name__)
app.secret_key = 'Enikeev-project2-secret-phrase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

goals = db.session.query(Goal).all()

@app.route('/')
def main():
    message_to_user = 'Свободны прямо сейчас'
    random_teachers = random.sample(db.session.query(Teacher).all(), 6)
    return render_template('index.html', goals=goals, teachers=random_teachers, user_message=message_to_user)

@app.route('/all/')
def main_all_teachers():
    message_to_user = 'Представляем Вашему вниманию всех наших преподавателей'
    teachers = db.session.query(Teacher).all()
    return render_template('index.html', goals=goals, teachers=teachers, user_message=message_to_user)

@app.route('/goals/<goal>')
def render_goals(goal):
    goal_result = db.session.query(Goal).filter(Goal.goalTitle_eu == goal)
    teachers_result = db.session.query(Teacher).filter(Teacher.goals.contains(goal_result.scalar())).order_by(
        Teacher.rating.desc())
    return render_template('goal.html', teachers=teachers_result, goal=goal_result)

@app.route('/profiles/<id_teacher>')
def render_profile_teacher(id_teacher=1):
    teacher_id = int(id_teacher)
    free_time_counter = 0
    bisy_days = []
    teacher = db.session.query(Teacher).filter(Teacher.id == teacher_id).first_or_404(description='Такой страницы нет')
    teacher_free = json.loads(teacher.free)
    for day in teacher_free:
        for time in teacher_free[day]:
            if teacher_free[day][time] == True:
                free_time_counter += 1
        if free_time_counter == 0:
            bisy_days.append(day)
        free_time_counter = 0
    return render_template('profile.html', teacher=teacher, free=teacher_free, bisy_days=bisy_days, week=week)

"""@app.route('/request/')
def render_request():
    return render_template('request.html', free_time=client_free_time, goals=goals)

@app.route('/request_done/', methods=['POST'])
def render_request_done():
    client_request_info = {"clientName": request.form["clientName"],
                           "clientPhone": request.form["clientPhone"],
                           "clientGoal": request.form["goal"],
                           "clientTime": request.form["time"]}
    add_aplication("request.json", client_request_info)
    return render_template('request_done.html', client=client_request_info, goals=goals)"""

@app.route('/booking/<id_teacher>/<day>/<time>/', methods=['GET', 'POST'])
def render_booking(id_teacher, day, time):
    teacher_id = int(id_teacher)
    lesson_time = {"day": day, "time": time}
    teacher = db.session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if request.method == 'POST':
        booking_form = BookingForm()

        clientName = booking_form.clientName.data
        clientPhone = booking_form.clientPhone.data
        clientWeekday = booking_form.clientWeekday.data
        clientTime = booking_form.clientTime.data
        clientTeacher_id = booking_form.clientTeacher.data
        clientTeacher = db.session.query(Teacher).filter(Teacher.id == clientTeacher_id).first()

        client_booking = Booking(clientName=clientName,
                                 clientPhone=clientPhone,
                                 clientWeekday=clientWeekday,
                                 clientTime=clientTime,
                                 clientTeacher=clientTeacher)
        db.session.add(client_booking)
        db.session.commit()
        return render_template('booking_done.html', client=client_booking, week=week)
    else:
        booking_form = BookingForm()
        return render_template('booking.html', form=booking_form, teacher=teacher, lesson_time=lesson_time, week=week)

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'


if __name__ == '__main__':
    app.run()
