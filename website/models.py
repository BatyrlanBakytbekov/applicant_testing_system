from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(15))
    has_taken_test = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')


class Skills(db.Model):
    applicant_skill_id = db.Column(db.Integer, primary_key=True)
    programminglang = db.Column(db.String(15))
    engineeringskill = db.Column(db.String(15))
    itskill = db.Column(db.String(15))
    managementskill = db.Column(db.String(15))
    marketingskill = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(30), unique=False)
    question_id = db.Column(db.Integer)
    correct_answer = db.Column(db.String(30))
    applicant_answer = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(30), db.ForeignKey('answers.test_name'))
    name = db.Column(db.String(150), db.ForeignKey('user.first_name'))
    score = db.Column(db.Integer)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    question = db.Column(db.String(255))
    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))
    correct_answer = db.Column(db.String(100))