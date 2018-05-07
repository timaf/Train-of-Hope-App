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
        if not request.form['title'] or not request.form['location'] or not request.form['description'] or not request.form['date'] or not request.form['time']:
            flash('Please enter all the fields', 'error')
        else:
            # Update events table
            event = Event(request.form['title'], request.form['location'],
            request.form['description'], request.form['date'], request.form['time'])
            db.session.add(event)
            db.session.commit()

            skill = Competence(request.form['skill0'], event.id)
            db.session.add(skill)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('eventCreation.html')





