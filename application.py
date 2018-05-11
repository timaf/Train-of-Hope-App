from flask import Flask, flash, redirect, url_for, render_template, request,jsonify, session
from werkzeug.exceptions import default_exceptions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from datetime import date
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

    # Query database for the future events and competences
    today = date.today()
    updated_events = Event.query.filter(Event.date >= today).all()
    db.session.commit()

    # Find remaining skills
    remaining_skills = []
    for updated_event in updated_events:
        print(updated_events)
        print(updated_event.competence)
        #if updated_event.competence.coming_skill == Null:
            #remaining_skills.append[updated_event.competence.nedded_skill]

    return render_template("nina.html", events=updated_events, remaining_skills=remaining_skills)

@app.route('/event_creation', methods = ['GET', 'POST'])
def event_creation():

    # Forget any event_id
    session.clear()

    if request.method == 'POST':

        event_detail = request.form
        if not event_detail['title'] or not event_detail['location'] or not event_detail['description'] or not event_detail['date'] or not event_detail['time']:
            flash('Please enter all the fields', 'error')

        else:
            # Validating date column becausse SQLite Date type only accepts Python date objects as input
            valid_date = datetime.strptime( event_detail['date'], '%d/%m/%Y').date()

            # Update events table
            event = Event(event_detail['title'], event_detail['location'],
            event_detail['description'], valid_date, event_detail['time'])
            db.session.add(event)
            db.session.commit()

            # Update competences table
            skills = event_detail.getlist('skill')
            for skill in skills:
                event_skill = Competence(skill, Null, event.id)
                db.session.add(event_skill)
                db.session.commit()
            flash('Event was successfully added')

            # Remember which event
            session["my_event_id"] = event.id

            return redirect(url_for('event_voting'))

    return render_template('event_creation.html')


@app.route('/event_voting', methods = ['GET', 'POST'])
def event_voting():

    if request.method == 'POST':
        coming_competence = request.form

        if coming_competence :

             # Update competences table
            coming_skills = coming_competence.getlist('coming_skill')
            the_event_competences = Competence.query.filter(Competence.event_id == session["my_event_id"]).all()
            for coming_skill in coming_skills:
                for the_event_competence in the_event_competences:
                    if coming_skill == the_event_competence.needed_skill:
                        the_event_competence.coming_skill = coming_skill
                        db.session.commit()

        return redirect(url_for('show_all'))

    else :
        # upload the event to vote
        my_event = Event.query.filter(Event.id == session["my_event_id"]).first()
        db.session.commit()
        return render_template("volunteer.html", my_event=my_event)







