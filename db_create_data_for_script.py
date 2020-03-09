from data import teachers, goals
from db_create_script import Teacher, Goal
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open('teachers_data.json', 'w') as f:
    json.dump(teachers, f)

with open("teachers_data.json", "r") as f:
    teachers_json = json.load(f)

for teacher in teachers_json:
    teacher_db = Teacher(name=teacher['name'],
                         about=teacher['about'],
                         rating=teacher['rating'],
                         picture=teacher['picture'],
                         price=teacher['price'],
                         free=json.dumps(teacher['free']))
    db.session.add(teacher_db)
    for goal in teacher['goals']:
        goal_for_teachers = db.session.query(Goal).filter(Goal.goalTitle_eu == goal).first()
        if goal_for_teachers is None:
            goal_db = Goal(goalTitle_eu=goal,
                           goalTitle_ru=goals[goal])
            db.session.add(goal_db)
            goal_for_teachers = goal_db
        goal_for_teachers.teachers.append(teacher_db)


db.session.commit()