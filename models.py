from TrainOfHope import os, db
from datetime import datetime



class Event(db.Model):

    __tablename__ = "events_detail"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.Text,nullable=False)
    location = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    skills = relationship("Competences")



    def __init__(self, title, location, description, date):
        self.title = title
        self.location = location
        self.description = description
        self.date = date

class Competences(db.Model):

    __tablename__ = "competences"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    needed_skill = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer,nullable=False)
    events_id = db.Column(db.Integer, nullable=False, ForeignKey("events_detail.id"))

    def __init__(self, skill, number, events_id):
        self.skill = skill
        self.number = number
        self.events_id = events_id
