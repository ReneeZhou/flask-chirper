from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    message = TextAreaField('message', validators = [DataRequired(), Length(max = 600)])
    submit = SubmitField('Submit')