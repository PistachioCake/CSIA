from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SchoolForm

from collections import namedtuple

Team = namedtuple('Team', ['name', 'password'])
School = namedtuple('School', ['name', 'teams'])
comp1 = [
    School("Westwood", [
        Team("Westwood #1", "never"),
        Team("Westwood #2", "gonna"),
        Team("Westwood #3", "give-"),
        Team("Westwood #4", "youup"),
    ]),
    School("West Lake", [
        Team("West Lake #1", "never"),
        Team("West Lake #2", "gonna"),
        Team("West Lake #3", "let--"),
        Team("West Lake #4", "you--"),
        Team("West Lake #5", "down-"),
    ]),
    School("Cedar Park", [
        Team("Cedar Park #1", "never"),
        Team("Cedar Park #2", "gonna"),
        Team("Cedar Park #3", "run--"),
        Team("Cedar Park #4", "aroun"),
        Team("Cedar Park #5", "d-and"),
        Team("Cedar Park #6", "deser"),
        Team("Cedar Park #7", "t-you"),
    ]),
]

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    form = SchoolForm()
    if form.validate_on_submit():
        flash(f'School inputted: School name {form.school_name.data}, with {form.no_of_teams.data} number of teams.')
        return redirect(url_for('index'))
    return render_template("teams.html", title="Teams", competition=comp1, form=form)

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
