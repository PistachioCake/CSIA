from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import SchoolForm, EditTeamForm
import app.models as models


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    comp1 = models.Competition.query.filter_by(name="comp1").first()
    if not comp1:
        comp1 = models.Competition(name="comp1")
        db.session.add(comp1)
        db.session.commit()

    # For the school form:
    add_school_form = SchoolForm()
    if add_school_form.submit_school.data and add_school_form.validate_on_submit():
        flash(f'School inputted: School name {add_school_form.school_name.data}, with {add_school_form.no_of_teams.data} teams.')
        # Create a school associated with the competition
        school = models.School(name=add_school_form.school_name.data, competition=comp1)
        # Add this school to the database
        db.session.add(school)
        for i in range(add_school_form.no_of_teams.data):
            # Create a team associated with the school
            team = models.Team(name=f"{add_school_form.school_name.data} #{i}", password="foobar", school=school)
            # Add this team to the database
            db.session.add(team)
        # Commit data to persistent storage
        db.session.commit()
    
    # For the team form
    edit_team_form = EditTeamForm()
    if edit_team_form.submit_password.data and edit_team_form.is_submitted():
        if edit_team_form.validate():
            team = models.Team.query.get(edit_team_form.team_id.data)
            flash(f'Team {team.name} updated: Password changed from {team.password} to {edit_team_form.password.data}')
            team.password = edit_team_form.password.data
            db.session.commit()
        else:
            flash(f'Unable to update team.')
            flash(f'{edit_team_form.errors}')

    if edit_team_form.submit_delete.data and edit_team_form.is_submitted():
            team = models.Team.query.get(edit_team_form.team_id.data)
            flash(f'Team {team.name} deleted.')
            db.session.delete(team)
            db.session.commit()

    return render_template("teams.html", title="Teams", competition=comp1, add_school_form=add_school_form, edit_team_form=edit_team_form)

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
