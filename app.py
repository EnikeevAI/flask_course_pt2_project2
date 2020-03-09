from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from db_create_script import Teacher, Goal, teachers_goals_association
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

goals = db.session.query(Goal).all()
week = {"monday": "Понедельник",
        "tuesday": "Вторник",
        "wednesday": "Среда",
        "thursday": "Четверг",
        "friday": "Пятница",
        "saturday": "Суббота",
        "sunday": "Воскресенье"}

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
    goal_result = db.session.query(Goal).filter(Goal.goalTitle_eu==goal)
    goal_id = db.session.query(Goal).filter(Goal.goalTitle_eu==goal).scalar()
    print('goal_id', goal_id)

    teachers_result = db.session.query(Teacher).filter(Teacher.goals.contains(goal_id)).order_by(Teacher.rating.desc())
    #teachers_result = db.session.query(Teacher).filter(Teacher.)
    #for t in teachers_result:
        #print(t.rating)
        #print(t.goals)
    #test.order_by(Teacher.rating)

    #test = db.session.query(Teacher).filter(Teacher.id.in_(goal_id.teachers)).order_by(Teacher.rating)
    '''for t in test:
        
    teachers_result = db.session.query(Teacher).filter(Teacher.id.in_(
        db.session.query(Goal).filter(Goal.goalTitle_eu==goal))).all()
    goal_reasult = db.session.query(Goal).filter(Goal.goalTitle_eu==goal)
    if goal not in goals:
        return page_not_found(404)
    for teacher in teachers_json:
        if goal in teacher['goals']:
            find_teachers_rating[teacher['id']] = teacher['rating']
    for teacher_id_and_rating in sorted(find_teachers_rating.items(),
                                        key=lambda rating_sort_param: -rating_sort_param[1]):
        for teacher in teachers_json:
            if teacher_id_and_rating[0] == teacher['id']:
                teachers_result.append(teacher)'''
    return render_template('goal.html', teachers=teachers_result, goal=goal_result)

@app.route('/profiles/<id_teacher>')
def render_profile_teacher(id_teacher=1):
    teacher_id = int(id_teacher)
    free_time_counter = 0
    bisy_days = []
    teacher = db.session.query(Teacher).filter(Teacher.id==teacher_id).first_or_404(description='Такой страницы нет')
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
    return render_template('request_done.html', client=client_request_info, goals=goals)

@app.route('/booking/<id_teacher>/<day>/<time>/')
def render_booking(id_teacher, day, time):
    teacher_id = int(id_teacher)
    lesson_time = {"day": day, "time": time}
    teacher_json = find_teacher_json(teacher_id)
    return render_template('booking.html', teacher=teacher_json, lesson_time=lesson_time, week=week)

@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    client_booking_info = {"clientName": request.form["clientName"],
                           "clientPhone": request.form["clientPhone"],
                           "clientTeacher": request.form["clientTeacher"],
                           "clientWeekday": request.form["clientWeekday"],
                           "clientTime": request.form["clientTime"]}

    add_aplication("booking.json", client_booking_info)
    return render_template('booking_done.html', client=client_booking_info, week=week)"""

@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'

if __name__ == '__main__':
    app.run()
