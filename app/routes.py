from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SchoolForm, EditTeamForm, EditSchoolForm
from app import actions

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

    # For the add school form:
    add_school_form = SchoolForm()
    if add_school_form.submit_new_school.data and add_school_form.validate_on_submit():
        flash(f'School inputted: School name {add_school_form.school_name.data}, with {add_school_form.no_of_teams.data} teams.')
        actions.add_school(comp1, add_school_form.school_name.data, add_school_form.no_of_teams.data)
    
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

    if edit_school_form.add_team_to_school.data and edit_school_form.is_submitted():
        print(edit_school_form.data)
        school = actions.get_school(id=edit_school_form.school_id.data)
        flash(f'Added a team to {school.name}.')
        actions.add_team(school)

        
    return render_template("teams.html", title="Teams", 
        competition=comp1, 
        add_school_form=add_school_form, 
        edit_team_form=edit_team_form, 
        edit_school_form=edit_school_form)

@app.route('/admins')
def admins():
    return render_template("admins.html", title="Admins", page_name="Admins")
