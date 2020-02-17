from app import db

# should display_name be more specific to the class itself?
# ie. Competition.display_name -> Competition.competition_name

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(64), index=True, unique=True)
    schools = db.relationship('School', backref='competition name', lazy='dynamic')

    def __repr__(self):
        return f"<Competition {self.display_name} with x schools>"

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(64), index=True, unique=True)
    teams = db.relationship('Team', backref='school name', lazy='dynamic')
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

    def __repr__(self):
        return f"<School {self.display_name} with x teams>"
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(64), unique=True) # TODO?: Does this need a unique=True or a index=True?
    team_num = db.Column(db.Integer, index=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    def __repr__(self):
        return f"<Team {self.display_name} from school {school_id}>"
    
