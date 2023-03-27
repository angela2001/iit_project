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
    _tablename_ = 'shows'
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String)
    time = db.Column(db.String)
    availability=db.Column(db.Integer)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'))


class Venue(db.Model):
    _tablename_ = 'venue'
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String)
    capacity = db.Column(db.Integer)


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
        validlogin = db.session.query(Admin).filter(
            Admin.admin_name == username, Admin.password == password).first()
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
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        venueDict={}
        conn = sqlite3.connect("database.sqlite3")
        cur = conn.cursor()
        query = """SELECT venue_id,venue_name,location from venue"""
        cur.execute(query)
        venues = cur.fetchall()
        for venue in venues:
            query2 = """SELECT show_name,availability from shows where venue_id=?"""
            cur.execute(query2, (venue[0],))
            shows=cur.fetchall()
            venueDict[venue[0]]=[venue[1],shows,venue[2]] 
        # print(venueDict)    
        cur.close()
        return render_template("home.html", venueDict=venueDict)
    if request.method == 'POST':
        venueDict={}
        if 'venueSearch' in request.form:
            location = request.form['venuelocation']
            conn = sqlite3.connect("database.sqlite3")
            cur = conn.cursor()
            query = """SELECT venue_id,venue_name,location from venue WHERE location=?"""
            cur.execute(query,(location,))
            venues = cur.fetchall()
            for venue in venues:
                query2 = """SELECT show_name,availability from shows where venue_id=?"""
                cur.execute(query2, (venue[0],))
                shows=cur.fetchall()
                venueDict[venue[0]]=[venue[1],shows,venue[2]]    
            cur.close()
            return render_template("home.html", venueDict=venueDict)
    # if request.method == 'GET':
    #     conn = sqlite3.connect("database.sqlite3")
    #     cur = conn.cursor()
    #     query = """SELECT venue_name from venue"""
    #     cur.execute(query)
    #     venues = cur.fetchall()
    #     cur.close()
    #     return render_template("home.html", venues=venues)
    # if request.method == 'POST':
    #     if 'venueSearch' in request.form:
    #         location = request.form['venuelocation']
    #         conn = sqlite3.connect("database.sqlite3")
    #         cur = conn.cursor()
    #         query = """SELECT venue.venue_name, shows.show_name from venue inner join shows on venue.venue_id=shows.venue_id WHERE location=?"""
    #         #show_query="""SELECT show_name from show WHERE """
    #         cur.execute(query,(location,))
    #         rows = cur.fetchall()
    #         cur.close()
    #         print(rows)
    #         if (len(rows)==0):
    #             rows=[("No venues currently in this location hosting shows","No shows")]
    #         return render_template("home.html", venues=rows)

        

@app.route('/admin_home', methods=['GET'])
def admin_home():
    venueDict={}
    conn = sqlite3.connect("database.sqlite3")
    cur = conn.cursor()
    query = """SELECT venue_id,venue_name,location from venue"""
    cur.execute(query)
    venues = cur.fetchall()
    for venue in venues:
        query2 = """SELECT show_name,availability,show_id from shows where venue_id=?"""
        cur.execute(query2, (venue[0],))
        shows=cur.fetchall()
        venueDict[venue[0]]=[venue[1],shows,venue[2]] 
    print(venueDict)    
    cur.close()
    return render_template("admin_home.html", venueDict=venueDict)

@app.route('/admin/add_venue', methods=['GET','POST'])
def addVenue():
    if request.method == 'GET':
        return render_template('add_venue.html')
    if request.method == 'POST':
        venue_name = request.form['venue_name']
        location = request.form['location']
        capacity=request.form['capacity']
        venue = Venue(venue_name=venue_name, location=location, capacity=capacity)
        db.session.add(venue)
        db.session.commit()
        return redirect('/admin_home')

@app.route('/admin/edit_venue/<venue_id>',methods=['GET','POST'])
def editVenue(venue_id):
    if request.method == 'GET':
        return render_template('edit_venue.html')
    if request.method == 'POST':
        venue_id=venue_id
        venue_name = request.form['venue_name']
        location = request.form['location']
        capacity=request.form['capacity']
        # venue = Venue(venue_name=venue_name, location=location, capacity=capacity)
        # db.session.add(venue)
        # db.session.commit()
        conn = sqlite3.connect("database.sqlite3")
        cur = conn.cursor()
        sql="""update table venue set venue_name=?, location=?,capacity=? where venue_id=?"""
        cur.execute(sql,(venue_name,location,capacity,venue_id))
        venues = cur.fetchall()
        return redirect('/admin_home')
    
@app.route('/admin/add_show',methods=['GET','POST'])
def addShow():
    if request.method == 'GET':
        return render_template('add_show.html')
    if request.method == 'POST':
        show_name = request.form['show_name']
        rating = request.form['rating']
        price=request.form['price']
        date=request.form['date']
        time=request.form['time']
        availability=request.form['availability']
        venue_id=request.form['venue_id']
        show = Shows(show_name=show_name, rating=rating, price=price,date=date,time=time,availability=availability,venue_id=venue_id)
        db.session.add(show)
        db.session.commit()
        return redirect('/admin_home')
    
@app.route('/admin/edit_show/<show_id>',methods=['GET','POST'])
def editShow(show_id):
    if request.method == 'GET':
        return render_template('edit_show.html',show_id=show_id)
    if request.method == 'POST':
        show_name = request.form['show_name']
        rating = request.form['rating']
        price=request.form['price']
        date=request.form['date']
        time=request.form['time']
        availability=request.form['availability']
        venue_id=request.form['venue_id']
        # venue = Venue(venue_name=venue_name, location=location, capacity=capacity)
        # db.session.add(venue)
        # db.session.commit()
        conn = sqlite3.connect("database.sqlite3")
        cur = conn.cursor()
        sql="""update table shows set show_name=?, rating=?, price=?, date=?, time=? ,availability=?, venue_id=? where show_id=?"""
        cur.execute(sql,(show_name,rating,price,date,time,availability,venue_id,show_id))
        venues = cur.fetchall()
        return redirect('/admin_home')

@app.route('/admin/delete_show/<sid>',methods=['GET'])
def deleteShow(sid):
    conn = sqlite3.connect("database.sqlite3")
    cur = conn.cursor()
    sql="""DELETE FROM shows WHERE show_id=?"""
    cur.execute(sql,(sid,))
    conn.commit()
    return redirect('/admin_home')

@app.route('/admin/delete_venue/<venue_id>',methods=['GET'])
def deleteVenue(venue_id):
    conn = sqlite3.connect("database.sqlite3")
    cur = conn.cursor()
    sql="""DELETE FROM venue WHERE venue_id=?"""
    cur.execute(sql,(venue_id,))
    conn.commit()
    return redirect('/admin_home')

# @app.route('/book_ticket',methods=['GET','POST'])
# def bookTicket():  

# Run app
if __name__ == "__main__":
    app.run(debug=True)
