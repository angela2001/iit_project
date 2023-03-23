from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
# import sqlite3
# from sqlalchemy.sql import func
# from flask_restful import Resource,Api

# App
app = Flask(__name__)

# SqlAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
# API calls
# api = Api(app)
# app.app_context().push()

# Creating model tables


class User(db.Model):
    _tablename_ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # score = db.Column(db.Integer, default = 0)
    # udeck = db.relationship('Deck', cascade='all, delete-orphan', backref='deck')


# class Deck(db.Model):
#     __tablename__ = 'deck'
#     deck_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
#     deckname = db.Column(db.String, unique=True, nullable=False)
#     user = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     score = db.Column(db.Integer, default=0)
#     last_rev = db.Column(db.DateTime(timezone=True), default=func.now())
    # dcard = db.relationship('Card', cascade='all, delete-orphan', backref='card')

class Card(db.Model):
    _tablename_ = 'card'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deckname = db.Column(db.String, nullable=False)
    # deck = db.Column(db.String, db.ForeignKey('deck.deckname'), nullable = False)
    front = db.Column(db.String)
    back = db.Column(db.String)

# Login


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validlogin = db.session.query(User).filter(User.username == username, User.password == password).first()
        if validlogin:
            return redirect('/home'.format(username))
        return render_template('invalid_login.html')

# Sign-up page


@app.route('/signup', methods=['GET', 'POST'])
def signinpage():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userexists = db.session.query(User).filter(User.username == username).first()
        if userexists:
            return render_template('user_exists.html')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')


# Home page
@app.route('/home', methods=['GET'])
def Flashcard():
    return render_template("base.html")


# Run app
if __name__ == "__main__":
    app.run(debug=True)
