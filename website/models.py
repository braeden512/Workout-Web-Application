from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #id of a particular recorded exercise
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)  #how much weight is loaded
    type_of_exercise = db.Column(db.String(50)) #the type of exercise (benchpress)
    text = db.Column(db.String(10000))    #personal notes abt an exercise
    date = db.Column(db.String)    #date the exercise is recorded
    time = db.Column(db.String)   #time the exercise is recorded
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #associate exercise with a particular user
    onerepmax = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    weight = db.Column(db.Integer)
    exercises = db.relationship('Exercise')

#possible to add more and relate them to user