from app import db

# should name be more specific to the class itself?
# ie. Competition.name -> Competition.competition_name

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    schools = db.relationship('School', backref='competition', lazy='dynamic')

    def __repr__(self):
        return f"<Competition {self.name} with {len(self.schools.all())} schools>"

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    teams = db.relationship('Team', backref='school', lazy='dynamic')
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

    def __repr__(self):
        return f"<School {self.name} with {len(self.teams.all())} teams>"
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True) # TODO?: Does this need a unique=True or a index=True?
    password = db.Column(db.String(64))
    team_num = db.Column(db.Integer, index=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return f"<Team {self.name} with password {self.password}>"
    
