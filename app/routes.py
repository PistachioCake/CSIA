from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SchoolForm

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/forms', methods=['GET', 'POST'])
def forms():
    form = SchoolForm()
    if form.validate_on_submit():
        flash(f'School inputted: School name {form.school_name}, with {form.no_of_teams} number of teams.')
        return redirect(url_for('index'))
    return render_template("forms.html", title="School Input", form=form)
