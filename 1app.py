from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime




from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Flask-SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
db.init_app(app)
class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.Text,unique=True,nullable=False)
    hash = db.Column(db.Text,nullable=False)
    cash= db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None), nullable=False)

    def __init__(self, username, hash, cash):
        self.username = username
        self.hash = hash
        self.cash = cash

class History(db.Model):

    __tablename__ = "history"
    history_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    symbol = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text,nullable=False)
    shares = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float,nullable=False)
    total = db.Column(db.Float,nullable=False)
    theDate = db.Column(db.DateTime, nullable=False)
    id = db.Column(db.Integer, nullable=False)

    def __init__(self, symbol, name, shares, price, total, theDate, id):
        self.symbol = symbol
        self.name = name
        self.shares = shares
        self.price = price
        self.total = total
        self.theDate = theDate
        self.id = id

db.create_all()

@app.route("/")
@login_required
def index():

    # How much cash the user have
    left_cash = User.query.get(session["user_id"])

    # Query for all the transactions the user made
    user_transaction = History.query.with_entities(History.symbol, func.sum(History.shares))\
    .filter(History.id == session["user_id"]).group_by(History.symbol)
    db.session.commit()

    properties_price = 0
    transactions = []

    if user_transaction:
        for transaction in user_transaction:
            if transaction[1] != 0:
                # Look up quote for symbol
                stock = lookup(transaction[0])

                # Calculate all the current stock cost
                stock_total = transaction[1] * stock["price"]

                # Calculate the user's properties of stocks
                properties_price += stock_total

                # Adding the updated values to the dictionary stock in order to print them in the main page
                stock["shares"] = transaction[1]
                stock["total"] = stock_total

                # Putting all the transactions in one list
                transactions.append(stock)

        # Adding the left money cash to the use's proporties
        properties_price += left_cash.cash

    return render_template("main.html", transactions=transactions, left_cash1=left_cash.cash,
                           properties_price=properties_price)




@app.route("/history")
@login_required
def history():
    history_query = History.query.filter(History.id == session["user_id"])
    return render_template("history.html", history_query=history_query)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = User.query.filter(User.username == request.form.get("username"))

        # Ensure username exists and password is correct
        if rows is None or not check_password_hash(rows[0].hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username", 400)

        passd = request.form.get("password")
        # Ensure password was submitted
        if not passd:
            return apology("missing password", 400)

        # Ensure the password is a strong one
        elif len(passd) < 8 or passd.isdigit() or passd.isalpha() or not passd.isprintable():
            return apology("password must be at least a mix of 8 letters,symbols and numbers", 400)

        # Ensure confirmation passsword was submitted and it matches the password
        elif not request.form.get("confirmation") or passd != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Query database for the username
        register_row = User.query.filter(User.username == request.form.get("username")).first()

        # Ensure the same username dosn't exists
        if register_row != None:
            return apology("username taken", 400)

        # Store the username and hashed password in a variable
        the_user = request.form.get("username")
        hash2 = generate_password_hash(request.form.get("password"))

        # Insert the new user into table users
        new_row = User(the_user, hash2, 10000.00)
        db.session.add(new_row)
        db.session.commit()

        # Remember which user has registerd in
        session["user_id"] = new_row.id

        # Flash a massage after doing everything right
        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # When via GET
    else:
        return render_template("register.html")

    return render_template("sell.html", sell_query=sell_query)
