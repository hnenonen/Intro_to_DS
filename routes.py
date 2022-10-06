from app import app
import service
from flask import render_template, request, redirect, session, abort

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["GET","POST"])
def evaluate():
    text = request.form["inputOverview"]
    if len(text) == 0 or len(text) >10000:
        return render_template("error.html", message="Overview too short or too long")
    else:
        #worth_watch = "BAD"
        #estimated_runtime = 180 
        #estimated_gross = 9999
        #estimated_voteaverage = 5.0
        
        worth_watch, estimated_runtime, estimated_gross, estimated_voteaverage = service.evaluate(text)
        recommendation_list = service.recommendation()
        return render_template("evaluate.html", text=text, worth_watch = worth_watch, recommendation_list = recommendation_list, estimated_runtime=estimated_runtime, estimated_gross=estimated_gross, estimated_voteaverage=estimated_voteaverage)
