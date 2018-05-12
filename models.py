from TrainOfHope import os, db
from datetime import datetime



class Event(db.Model):

    __tablename__ = "events"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.Text,nullable=False)
    location = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=True)
    time = db.Column(db.Text, nullable=True)
    competence = db.relationship("Competence", order_by="Competence.id", backref="events")

    def __init__(self, title, location, description, date, time):
        self.title = title
        self.location = location
        self.description = description
        self.date = date
        self.time = time

class Competence(db.Model):

    __tablename__ = "competences"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    needed_skill = db.Column(db.Text, nullable=False)
    coming_skill = db.Column(db.Text, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'),  nullable=False)



    def __init__(self, needed_skill, coming_skill, event_id):
        self.needed_skill = needed_skill
        self.coming_skill = coming_skill
        self.event_id = event_id

