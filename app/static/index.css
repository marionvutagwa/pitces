from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required
from ..models import User




class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    title = StringField('Pitch title',validators = [Required()])
    category =SelectField ('category',choices=[('business','business'),('job','job'),('interview','interview')])
    description = TextAreaField('')
    submit = SubmitField('Submit')   

class CommentForm(FlaskForm):
    description = StringField('Add here',validators = [Required()])
    submit = SubmitField('Submit')

class UpVote(FlaskForm): 
    submit = SubmitField('Submit')   

class DownVote(FlaskForm): 
    submit = SubmitField('Submit')  