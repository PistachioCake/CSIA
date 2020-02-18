from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class SchoolForm(FlaskForm):
    school_name = StringField('School name', validators=[DataRequired()])
    no_of_teams = IntegerField('Number of Teams', validators=[DataRequired()])
    submit = SubmitField('Add School')
    
