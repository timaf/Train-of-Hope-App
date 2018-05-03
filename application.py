from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from TrainOfHope import create_app, db

# Configure application
app = Flask(__name__)
app = create_app()

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


from TrainOfHope.models import Event, Competences
with app.app_context():
    db.create_all()


@app.route("/")
def index():

        # Query database for the updated events
        events = Event.query.all()

        # Query database for the competences
        #skills = Competences.query.filter_by(events_id == Event.id)

        return render_template("nina.html", events=events, skills=skills)







