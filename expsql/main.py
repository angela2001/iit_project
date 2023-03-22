from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"testdb.sqlite3")
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model):
    _tablename_='user',
    uid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    uname=db.Column(db.String, unique=True)
    email=db.Column(db.String, unique=True)
    
class ArticleAuthors(db.Model):
    _tablename_='article_authors',
    uid=db.Column(db.Integer,db.ForeignKey("user.uid"), primary_key=True,nullable=False)
    aid=db.Column(db.Integer,db.ForeignKey("article.aid"), primary_key=True,nullable=False)
    
class Article(db.Model):
    _tablename_='article',
    aid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    title=db.Column(db.String)
    content=db.Column(db.String)
    authors=db.relationship("User", secondary="article_authors")
    

@app.route("/",methods=["GET","POST"])
def articles():
    articles=Article.query.all()
    return render_template("articles.html",articles=articles)

@app.route("/articlesBy/<username>",methods=["GET","POST"])
def articles_by_author(username):
    articles=Article.query.filter(Article.authors.any(uname=username))
    return render_template("articlesByAuthor.html",articles=articles,username=username)
    

if __name__=='__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )