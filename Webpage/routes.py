from app import app
from flask import render_template, request, redirect, session, abort

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["GET","POST"])
def evaluate():
    text = request.form["inputOverview"]
    

    worth_watch = "BAD"
    estimated_runtime = 180 
    estimated_gross = 9999
    estimated_voteaverage = 5.0

    # text for analysis 
    if len(text) > 100:
        worth_watch = "GOOD"
        estimated_runtime = 120
        estimated_gross = 239999
        estimated_voteaverage = 9.0


    
    return render_template("evaluate.html", text=text, worth_watch = worth_watch, estimated_runtime=estimated_runtime, estimated_gross=estimated_gross, estimated_voteaverage=estimated_voteaverage)
