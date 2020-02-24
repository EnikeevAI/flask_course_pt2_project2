from flask import Flask, render_template, request, url_for, redirect
import json
import pprint
from data import goals, teachers, week

app = Flask(__name__)

with open('teachers_data.json', 'w') as f:
    json.dump(teachers, f)


def find_teacher_json(teacher_id):
    with open("teachers_data.json", "r") as f:
        teachers_json = json.load(f)
    for teacher in teachers_json:
        if teacher['id'] == teacher_id:
            return teacher


@app.route('/')
def main():
    return "Здесь будет главная"
    # return render_template()


@app.route('/goals/<goal>')
def render_goals(goal):
    return "Здесь будет цель <goal>"
    # return render_template()


@app.route('/profiles/<id_teacher>')
def render_profile_teacher(id_teacher='1'):
    teacher_id = int(id_teacher)
    free_time_counter = 0
    bisy_days = []
    teacher_json = find_teacher_json(teacher_id)
    for day in teacher_json['free']:
        for time in teacher_json['free'][day]:
            if teacher_json['free'][day][time] == True:
                free_time_counter += 1
        if free_time_counter == 0:
            bisy_days.append(day)
        free_time_counter = 0
    return render_template('profile.html', teacher=teacher_json, bisy_days=bisy_days, goals=goals, week=week)


@app.route('/request/')
def render_request():
    return "Здесь будет заявка на подбор"
    # return render_template()


@app.route('/request_done/')
def render_request_done():
    return "Заявка на подбор отправлена"
    # return render_template()


@app.route('/booking/<id_teacher>/<day>/<time>/')
def render_booking(id_teacher, day, time):
    teacher_id = int(id_teacher)
    lesson_time = {"day": day, "time": time}
    teacher_json = find_teacher_json(teacher_id)
    return render_template('booking.html', teacher=teacher_json, lesson_time=lesson_time, week=week)


@app.route('/booking_done/', methods=['POST', 'GET'])
def render_booking_done():
    client_info = {"clientName": request.form["clientName"],
                   "clientPhone": request.form["clientPhone"],
                   "clientTeacher": request.form["clientTeacher"],
                   "clientWeekday": request.form["clientWeekday"],
                   "clientTime": request.form["clientTime"]}
    with open("booking.json", 'r') as f:
        applications = f.read()
        applications_json = json.loads(applications)
        applications_json.append(client_info)
        applications = json.dumps(applications_json)
    with open("booking.json", 'w') as f:
        f.write(applications)
    return render_template('booking_done.html', client=client_info, week=week)


@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'


if __name__ == '__main__':
    app.run()
