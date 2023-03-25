from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

current_dir = os.path.abspath(os.path.dirname(__file__))

# App
app = Flask(__name__)

# SqlAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"database.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

app.app_context().push()

# Creating model tables


class User(db.Model):
    _tablename_ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Admin(db.Model):
    _tablename_ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class Shows(db.Model):
    _tablename_='shows'
    show_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name= db.Column(db.String, unique=True, nullable=False)
    rating=db.Column(db.Integer)
    price=db.Column(db.Integer, nullable=False)
    date=db.Column(db.String)
    time =db.Column(db.String)
    venue_id=db.Column(db.Integer,db.ForeignKey('venue.venue_id'))
    
class Venue(db.Model):
    _tablename_='venue'
    venue_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name= db.Column(db.String, unique=True, nullable=False)
    location=db.Column(db.String)
    capacity =db.Column(db.Integer)


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
    

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        validlogin = db.session.query(Admin).filter(Admin.admin_name == username, Admin.password == password).first()
        if validlogin:
            return redirect('/admin_home'.format(username))
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
@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        conn = sqlite3.connect("database.sqlite3")
        cur = conn.cursor()
        query = """SELECT venue_name from venue"""
        cur.execute(query)
        venues = cur.fetchall()
        cur.close()
        return render_template("home.html", venues=venues)
    if request.method == 'POST':
        if 'venueSearch' in request.form:
            location = request.form['venuelocation']
            conn = sqlite3.connect("database.sqlite3")
            cur = conn.cursor()
            query = """SELECT venue_name from venue WHERE location=?"""
            cur.execute(query,(location,))
            rows = cur.fetchall()
            cur.close()
            return render_template("home.html", venues=rows)
        # elif 'remove_note_button' in request.form:

@app.route('/admin_home', methods=['GET'])
def admin_home():
    return render_template("admin_home.html")

@app.route('/admin_home', methods=['GET'])
def admin_home():
    return render_template("admin_home.html")


# Run app
if __name__ == "__main__":
    app.run(debug=True)
