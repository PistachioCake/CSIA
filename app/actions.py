from app import db
import app.models as models
from random import choice
import csv

# Should this be handled in a better way? Dynamically looked up or something?
with open('passwords.txt', 'r') as password_file:
    passwords = [password.strip() for password in password_file]

def commit_optional(f):
    def inner(*args, **kwargs):
        commit = kwargs.pop('commit', True)
        r = f(*args, **kwargs)
        if commit:
            db.session.commit()
        return r
    return inner

def get_competition(**kwargs):
    return models.Competition.query.filter_by(**kwargs).first()

@commit_optional
def get_or_make_competition(**kwargs):
    comp = models.Competition.query.filter_by(**kwargs).first()
    if not comp:
        comp = models.Competition(**kwargs)
        db.session.add(comp)
    return comp

@commit_optional
def add_school(competition, name, no_of_teams):
    prev = competition.schools.filter_by(name=name).first()
    if prev is not None:
        return False    # Don't overwrite a school that exists already
                        # TODO: Decide if there is a better way to do this
    # Create a school associated with the competition
    school = models.School(name=name, competition=competition)
    # Add this school to the database
    db.session.add(school)
    for i in range(no_of_teams):
        add_team(school, i+1, commit=False)
    return True

def get_school(**kwargs):
    return models.School.query.filter_by(**kwargs).first()

# is this needed?
def get_schools(**kwargs):
    return models.School.query.filter_by(**kwargs).all()

@commit_optional
def change_school_name(school, name):
    old_name = school.name
    school.name = name
    name += " "
    for team in school.teams:
        team.name = name + team.name.split()[-1]

@commit_optional
def reorganize_school(school):
    locked = [t.team_num for t in school.teams.filter_by(locked=True)]
    team_num = 0
    for team in school.teams.filter_by(locked=False):
        team_num += 1
        while team_num in locked:
            team_num += 1
        team.team_num = team_num

@commit_optional
def remove_school(school):
    for team in school.teams:
        remove_team(team)
    db.session.delete(school)

@commit_optional
def add_team(school, team_num=None, password=None, reorganize=True):
    if not password:
        password = choice(passwords)
    if not team_num:
        team_nums = [t.team_num for t in school.teams]
        team_num = 1
        while team_num in team_nums:
            team_num += 1
    
    team = models.Team(team_num=team_num, password=password, school=school)
    db.session.add(team)
    if reorganize:
        reorganize_school(school)

def get_team(**kwargs):
    return models.Team.query.filter_by(**kwargs).first()

def get_teams(**kwargs):
    return models.Team.query.filter_by(**kwargs).order_by(
                # models.Team.locked.desc(),
                models.Team.team_num).all()

@commit_optional
def change_team_password(team, new_password=None):
    if not new_password:
        new_password = choice(passwords)
    team.password = new_password

@commit_optional
def lock_team(team, account_num):
    team.account_num = account_num
    team.locked = True

@commit_optional
def remove_team(team, reorganize=True):
    db.session.delete(team)
    if reorganize:
        reorganize_school(team.school)

# =========
# Exports follow
# =========

def create_row(team, account_num, row=None):
    if not row:
        row = dict()
    row['account'] = 'team' + str(team.account_num)
    row['displayname'] = team.name
    row['password'] = team.password
    return row


def make_csv(competition, file):
    locked = [t.account_num for s in competition.schools for t in s.teams.filter_by(locked=True)]
    fieldnames = ['site', 'account', 'displayname', 'password', 'group', 'permdisplay', 'permlogin', 'externalid', 'alias', 'permpassword']
    default = {
        'site': '1',
        'group': 'TRUE',
        'permdisplay': 'TRUE',
        'permlogin': '',
        'externalid': '',
        'alias': '',
        'permpassword': '',
    }
    writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel-tab', lineterminator='\n')

    writer.writeheader()
    account_num = 0
    for school in competition.schools:
        for team in school.teams:
            if not team.locked:     # Don't change locked teams
                account_num += 1
                while account_num in locked:
                    account_num += 1
                lock_team(team, account_num)

            row = create_row(team, account_num, default)
            writer.writerow(row)

