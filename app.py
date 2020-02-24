from flask import Flask, render_template, request, url_for, redirect
import json
import pprint
from data import goals, teachers

app = Flask(__name__)

with open ('teachers_data.json', 'w') as f:
    json.dump(teachers, f)



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
    with open("teachers_data.json", "r") as f:
        teachers_json = json.load(f)
    for teacher in teachers_json:
        if teacher['id'] == teacher_id:
            teacher_json = teacher
    for day in teacher_json['free']:
        for time in teacher_json['free'][day]:
            if teacher_json['free'][day][time] == True:
                free_time_counter += 1
        if free_time_counter == 0:
            bisy_days.append(day)
        free_time_counter = 0
    pprint.pprint(bisy_days)
    return render_template('profile.html', teacher = teacher_json, bisy_days=bisy_days, goals=goals)

'''{% if True not in teacher.free %}
                                    
                                {% endif %}'''


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
    return "Здесь будет форма бронирования <id_teacher>"
    # return render_template()


@app.route('/booking_done/')
def render_booking_done():
    return "Заявка отправлена"
    # return render_template()


@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'


if __name__ == '__main__':
    app.run()
