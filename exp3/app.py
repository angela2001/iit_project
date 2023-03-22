from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

@app.route("/hello",methods=["GET","POST"])
def hello_world():
    if request.method=="GET":
        return render_template("getdetails.html")
    elif request.method=="POST":
        uname=request.form["name"]
        return render_template("displaydetails.html",display_name=uname)
    else:
        print("ERROR")
        

if __name__=='__main__':
    app.debug=True
    app.run()