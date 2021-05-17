from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators = [DataRequired(), Length(max = 280)])
    submit = SubmitField('Chirp')