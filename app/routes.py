from flask import render_template, flash, redirect, url_for, send_file
from app import app
from app.forms import SchoolForm, EditTeamForm, EditSchoolForm, AddTeamForm, DeleteAllSchoolsForm
from app import actions

from os import path

@app.route('/')
@app.route('/index')
def index():
    comp1 = actions.get_or_make_competition(name="comp1")
    # schools = actions.get_schools(competition=comp1)
    schools = comp1.schools.all()
    school_count = len(schools)
    team_count = 0
    for school in schools:
        team_count += len(school.teams.all())
    # db.session.query(Team).filter(Team.school.in_(schools)).count()
    return render_template("index.html", title="Home", school_count=school_count, team_count=team_count)

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    comp1 = actions.get_or_make_competition(name="comp1")

    # For the delete all schools form
    delete_all_schools_form = DeleteAllSchoolsForm()

    if delete_all_schools_form.delete_all_schools.data and delete_all_schools_form.is_submitted():
        for school in comp1.schools:
            actions.remove_school(school)
        flash(f'Deleted all schools.')

    # For the add school form:
    add_school_form = SchoolForm()

    if add_school_form.submit_new_school.data and add_school_form.validate_on_submit():
        added = actions.add_school(comp1, add_school_form.school_name.data, add_school_form.no_of_teams.data)
        if added: 
            flash(f'School inputted: School name {add_school_form.school_name.data}, with {add_school_form.no_of_teams.data} teams.')
        else:
            flash(f'Unable to add school {add_school_form.school_name.data}: School already exists.')
    
    # For the edit team form
    edit_team_form = EditTeamForm()

    if edit_team_form.submit_team.data and edit_team_form.is_submitted():
        if edit_team_form.validate():
            team = actions.get_team(id=edit_team_form.team_id.data)
            flash(f'Team {team.name} updated: Password changed from {team.password} to {edit_team_form.password.data}.')
            actions.change_team_password(team, edit_team_form.password.data)
        else:
            flash(f'Unable to update team.')
            flash(f'{edit_team_form.errors}')

    if edit_team_form.delete_team.data and edit_team_form.is_submitted():
        team = actions.get_team(id=edit_team_form.team_id.data)
        flash(f'Team {team.name} deleted.')
        actions.remove_team(team)

    # For the edit school form
    edit_school_form = EditSchoolForm()

    if edit_school_form.submit_school.data and edit_school_form.is_submitted():
        if edit_school_form.validate():
            school = actions.get_school(id=edit_school_form.school_id.data)
            flash(f'School {school.name} updated: Name changed to {edit_school_form.school_name.data}.')
            actions.change_school_name(school, edit_school_form.school_name.data)

    if edit_school_form.delete_school.data and edit_school_form.is_submitted():
        school = actions.get_school(id=edit_school_form.school_id.data)
        flash(f'School {school.name} deleted.')
        actions.remove_school(school)

    # For the add team form
    add_team_form = AddTeamForm()

    if add_team_form.add_team_to_school.data and add_team_form.is_submitted():
        school = actions.get_school(id=add_team_form.school_id.data)
        for _ in range(add_team_form.no_of_teams.data):
            actions.add_team(school)
        flash(f'Added {add_team_form.no_of_teams.data} team(s) to {school.name}.')
        
    return render_template("teams.html", title="Teams", 
        competition=comp1, 
        add_school_form=add_school_form, 
        edit_team_form=edit_team_form, 
        edit_school_form=edit_school_form, 
        add_team_form=add_team_form, 
        delete_all_schools_form=delete_all_schools_form,
        get_teams=actions.get_teams
        )

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")

@app.route('/export')
def export_csv():
    comp1 = actions.get_or_make_competition(name='comp1')
    p = path.join(app.config['FILE_DIRECTORY'], 'teams.csv')
    with open(p, 'w') as f:
        actions.make_csv(comp1, f)
    return send_file(p, mimetype='text/csv', as_attachment=True, attachment_filename='teams.csv')
