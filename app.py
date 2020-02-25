from flask import Flask, render_template, request, url_for, redirect
import json
import random
from data import goals, teachers, week, client_free_time

app = Flask(__name__)

with open('teachers_data.json', 'w') as f:
    json.dump(teachers, f)

with open("teachers_data.json", "r") as f:
    teachers_json = json.load(f)


def find_teacher_json(teacher_id, teachers=teachers_json):
    for teacher in teachers:
        if teacher['id'] == teacher_id:
            return teacher


def add_aplication(aplications_json_file_name, client_info):
    with open(aplications_json_file_name, 'r') as f:
        applications = f.read()
        applications_json = json.loads(applications)
        applications_json.append(client_info)
        applications = json.dumps(applications_json)
    with open(aplications_json_file_name, 'w') as f:
        f.write(applications)


@app.route('/')
def main():
    message_to_user = 'Представляем Вашему вниманию всех наших преподавателей'
    random_teachers = random.sample(teachers_json, 6)
    return render_template('index.html', goals=goals, teachers=random_teachers, user_message=message_to_user)

@app.route('/all/')
def main_all_teachers():
    message_to_user = 'Представляем Вашему вниманию всех наших преподавателей'
    return render_template('index.html', goals=goals, teachers=teachers_json, user_message=message_to_user)


@app.route('/goals/<goal>')
def render_goals(goal):
    find_teachers_rating = {}
    teachers_result = []
    if goal not in goals:
        return page_not_found(404)
    for teacher in teachers_json:
        if goal in teacher['goals']:
            find_teachers_rating[teacher['id']] = teacher['rating']
    for teacher_id_and_rating in sorted(find_teachers_rating.items(),
                                        key=lambda rating_sort_param: -rating_sort_param[1]):
        for teacher in teachers_json:
            if teacher_id_and_rating[0] == teacher['id']:
                teachers_result.append(teacher)
    return render_template('goal.html', teachers=teachers_result, goal=goals[goal])


@app.route('/profiles/<id_teacher>')
def render_profile_teacher(id_teacher='1'):
    teacher_id = int(id_teacher)
    free_time_counter = 0
    bisy_days = []
    teacher_json = find_teacher_json(teacher_id)
    if teacher_json == None:
        return page_not_found(404)
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
    return render_template('booking_done.html', client=client_booking_info, week=week)


@app.errorhandler(404)
def page_not_found(error):
    return 'Такой страницы нет'


if __name__ == '__main__':
    app.run()
