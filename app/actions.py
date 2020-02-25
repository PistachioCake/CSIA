from app import db
import app.models as models
from random import choice

# Should this be handled in a better way? Dynamically looked up or something?
with open('passwords.txt', 'r') as password_file:
    passwords = [password.strip() for password in password_file]

def get_competition(**kwargs):
    return models.Competition.query.filter_by(**kwargs).first()

def get_or_make_competition(**kwargs):
    comp = models.Competition.query.filter_by(**kwargs).first()
    if not comp:
        comp = models.Competition(**kwargs)
        db.session.add(comp)
        db.session.commit()
    return comp

def add_team(school, name, password=None, commit=True):
    if not password:
        password = choice(passwords)
    team = models.Team(name=name, password=password, school=school)
    db.session.add(team)
    if commit:
        db.session.commit()

def get_team(**kwargs):
    return models.Team.query.filter_by(**kwargs).first()

def get_teams(**kwargs):
    return models.Team.query.filter_by(**kwargs).all()

def change_team_password(team, new_password=None):
    if not new_password:
        new_password = choice(passwords)
    team.password = new_password
    db.session.commit()

def remove_team(team):
    db.session.delete(team)
    db.session.commit()

def add_school(competition, name, no_of_teams):
    # Create a school associated with the competition
    school = models.School(name=name, competition=competition)
    # Add this school to the database
    db.session.add(school)
    for i in range(no_of_teams):
        add_team(school, f'{name} #{i+1}', commit=False)
    # Commit data to persistent storage
    db.session.commit()

def get_school(**kwargs):
    return models.School.query.filter_by(**kwargs).first()

def get_schools(**kwargs):
    return models.School.query.filter_by(**kwargs).all()

def change_school_name(school, name):
    old_name = school.name
    school.name = name
    name += " "
    for team in school.teams:
        team.name = name + team.name.split()[-1]
    db.session.commit()

def remove_school(school):
    for team in school.teams:
        remove_team(team)
    db.session.delete(school)
    db.session.commit()
    
