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
        worth_watch, estimated_runtime, estimated_gross, estimated_voteaverage = service.evaluate(text)
        return render_template("evaluate.html", text=text, worth_watch = worth_watch, estimated_runtime=estimated_runtime, estimated_gross=estimated_gross, estimated_voteaverage=estimated_voteaverage)
