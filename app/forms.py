from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length
from wtforms_components import read_only

class SchoolForm(FlaskForm):
    school_name = StringField('School name', validators=[DataRequired()])
    no_of_teams = IntegerField('Number of Teams', validators=[DataRequired()])
    submit_new_school = SubmitField('Add School')
    
class EditTeamForm(FlaskForm):
    team_id = IntegerField('Team ID', id='team-id', validators=[DataRequired()])
    team_name = StringField('Team Name', id='team-name') # Should only be used to display stuff, not as an actual input mechanism
    password = StringField('Password', id='team-password', validators=[DataRequired(), Length(min=5)])
    submit_team = SubmitField('Update Team', default='team-update')
    delete_team = SubmitField('Delete Team', default='team-delete')

    def __init__(self, *args, **kwargs):
        super(EditTeamForm, self).__init__(*args, **kwargs)
        read_only(self.team_name)

class EditSchoolForm(FlaskForm):
    school_id = IntegerField('School ID', id='school-id', validators=[DataRequired()])
    school_name = StringField('School Name', id='school-name')
    submit_school = SubmitField('Update School', default='school-update')
    delete_school = SubmitField('Delete School', default='school-delete')

class AddTeamForm(FlaskForm):
    school_id = IntegerField('School ID', id='school-id', validators=[DataRequired()])
    no_of_teams = IntegerField('Number of Teams', default='1')
    add_team_to_school = SubmitField('Add Team to School', default='add-team') # Should this be in its own form?
