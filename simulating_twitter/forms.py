from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from simulating_twitter.models import User

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


    # create a custom validation
    # check whether username exists already
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one. ')
    
    # check whether email is already used
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one. ')


class LoginForm(FlaskForm):
    email = StringField('Email', \
        validators = [DataRequired(), Email()])
    password = PasswordField('Password',\
        validators = [DataRequired()])
    # remember = BooleanField('Remember Me') 
    # we will remember user by default unless they sign out manually
    submit = SubmitField('Log In')