from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SchoolForm
import app.models as models

comp1 = models.Competition.query.filter_by(name="comp1").first()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    form = SchoolForm()
    if form.validate_on_submit():
        flash(f'School inputted: School name {form.school_name.data}, with {form.no_of_teams.data} number of teams.')
        school = models.School(name=form.school_name.data)
        for i in range(form.no_of_teams.data):
            school.teams.append(models.Team(name=f"{form.school_name.data} #{i}", password="foobar"))
        comp1.schools.append(school)
    return render_template("teams.html", title="Teams", competition=comp1, form=form)

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
