from app import db
from sqlalchemy.ext.hybrid import hybrid_property

# should name be more specific to the class itself?
# ie. Competition.name -> Competition.competition_name

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    schools = db.relationship('School', backref='competition', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Competition {self.name} with {len(self.schools.all())} schools>"

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    teams = db.relationship('Team', backref='school', lazy='dynamic', cascade='all, delete-orphan')
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

    def __repr__(self):
        return f"<School {self.name} with {len(self.teams.all())} teams>"
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_num = db.Column(db.Integer, index=True, nullable=False)
    account_num = db.Column(db.Integer, index=True, nullable=True) # Should be null until locked == True
    # TODO Is this bad database design?
    password = db.Column(db.String(64))
    locked = db.Column(db.Boolean, default=False, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return f"<Team {self.name} with password {self.password}>"

    @hybrid_property
    def name(self):
        return self.school.name + " #" + str(self.team_num)
    
