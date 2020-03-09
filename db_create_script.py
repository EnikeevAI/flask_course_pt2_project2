from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enikeev_project2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

teachers_goals_association = db.Table('teachers_goals',
                                      db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                                      db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
                                      )

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.Text(1000), nullable=False)

    goals = db.relationship('Goal', secondary=teachers_goals_association, back_populates='teachers')
    teacher_bookings = db.relationship('Booking', back_populates='clientTeacher')

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    goalTitle_eu = db.Column(db.String(30), nullable=False)
    goalTitle_ru = db.Column(db.String(30), nullable=False)

    teachers = db.relationship('Teacher', secondary=teachers_goals_association, back_populates='goals')
    goal_requests = db.relationship('Request', back_populates='clientGoal')

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(50), nullable=False)
    clientPhone = db.Column(db.String(50), nullable=False, unique=True)
    clientWeekday = db.Column(db.String(50), nullable=False)
    clientTime = db.Column(db.String(10), nullable=False)

    clientTeacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    clientTeacher = db.relationship('Teacher', back_populates='teacher_bookings')

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(50), nullable=False)
    clientPhone = db.Column(db.String(50), nullable=False, unique=True)
    clientTime = db.Column(db.String(10), nullable=False)

    clientGoal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    clientGoal = db.relationship('Goal', back_populates='goal_requests')

db.create_all()

