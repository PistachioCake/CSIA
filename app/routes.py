from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SchoolForm, EditTeamForm
from app import actions

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    comp1 = actions.get_or_make_competition(name="comp1")

    # For the school form:
    add_school_form = SchoolForm()
    if add_school_form.submit_school.data and add_school_form.validate_on_submit():
        flash(f'School inputted: School name {add_school_form.school_name.data}, with {add_school_form.no_of_teams.data} teams.')
        actions.add_school(comp1, add_school_form.school_name.data, add_school_form.no_of_teams.data)
    
    # For the team form
    edit_team_form = EditTeamForm()
    if edit_team_form.submit_password.data and edit_team_form.is_submitted():
        if edit_team_form.validate():
            team = actions.get_team(id=edit_team_form.team_id.data)
            flash(f'Team {team.name} updated: Password changed from {team.password} to {edit_team_form.password.data}')
            actions.change_team_password(team, edit_team_form.password.data)
        else:
            flash(f'Unable to update team.')
            flash(f'{edit_team_form.errors}')

    if edit_team_form.submit_delete.data and edit_team_form.is_submitted():
            team = actions.get_team(id=edit_team_form.team_id.data)
            flash(f'Team {team.name} deleted.')
            actions.remove_team(team)

    return render_template("teams.html", title="Teams", competition=comp1, add_school_form=add_school_form, edit_team_form=edit_team_form)

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
