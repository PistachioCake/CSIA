from flask import render_template, flash, redirect, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/teams')
def teams():
    return render_template("teams.html", title="Teams", page_name="Teams")

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
