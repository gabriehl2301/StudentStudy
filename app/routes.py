from app import app 
from flask import render_template

@app.route("/StudySpace")
def Learnt():
    return render_template("LoginPage.html")



