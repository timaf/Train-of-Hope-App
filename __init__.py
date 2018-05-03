import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Flask-SQLAlchemy
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)

    return app