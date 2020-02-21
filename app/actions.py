from app import db
import app.models as models

def get_competition(**kwargs):
    return models.Competition.query.filter_by(**kwargs).first()

def get_or_make_competition(**kwargs):
    comp = models.Competition.query.filter_by(**kwargs).first()
    if not comp:
        comp = models.Competition(**kwargs)
        db.session.add(comp)
        db.session.commit()
    return comp

def get_team(**kwargs):
    return models.Team.query.filter_by(**kwargs).first()

def change_team_password(team, new_password):
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
        # Create a team associated with the school
        team = models.Team(name=f"{name} #{i+1}", password="foobar", school=school)
        # Add this team to the database
        db.session.add(team)
    # Commit data to persistent storage
    db.session.commit()