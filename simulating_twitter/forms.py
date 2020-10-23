from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', \
        validators = [DataRequired(), Length(min = 2, max = 20)])
    # phone = IntegerField('Phone', \
    #     validators = [DataRequired()])
    email = StringField('Email', \
        validators = [DataRequired(), Email()])
    password = PasswordField('Password', \
        validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Passrowd', \
        validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', \
        validators = [DataRequired(), Email()])
    password = PasswordField('Password',\
        validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')