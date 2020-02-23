from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


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
    return "Здесь будет преподаватель <id_teacher>"
    # return render_template()


@app.route('/request/')
def render_request():
    return "Здесь будет заявка на подбор"
    # return render_template()


@app.route('/request_done/')
def render_request_done():
    return "Заявка на подбор отправлена"
    # return render_template()


@app.route('/booking/<id_teacher>/<day>/<time>/')
def render_booking():
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
