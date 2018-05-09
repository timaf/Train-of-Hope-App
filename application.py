from flask import Flask, flash, redirect, url_for, render_template, request,jsonify, session
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


from TrainOfHope.models import Event, Competence
with app.app_context():
    db.create_all()


@app.route("/")
def show_all():

    # Query database for the updated events and competences
    events = Event.query.all()
    db.session.commit()
    return render_template("nina.html", events=events)

@app.route('/eventCreation', methods = ['GET', 'POST'])
def eventCreation():
    if request.method == 'POST':
        event_detail = request.form
        if not event_detail['title'] or not event_detail['location'] or not event_detail['description'] or not event_detail['date'] or not event_detail['time']:
            flash('Please enter all the fields', 'error')

        else:
            # Update events table
            event = Event(event_detail['title'], event_detail['location'],
            event_detail['description'], event_detail['date'], event_detail['time'])
            db.session.add(event)
            db.session.commit()


            skills = event_detail.getlist('skill')
            for skill in skills:
                event_skill = Competence(skill, event.id)
                db.session.add(event_skill)
                db.session.commit()
            flash('Event was successfully added')
            return redirect(url_for('show_all'))

    return render_template('eventCreation.html')





