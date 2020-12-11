from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from simulating_twitter.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
    email = EmailField('Email', validators = [DataRequired(), Email()])
    
    # dob_y = DateField('Year', validators = [DataRequired(), NumberRange(min = 1990, max = datetime.utcnow().year)], format = '%Y')
    # dob_m = DateField('Month', validators = [DataRequired(), NumberRange(min = 1, max = 12)], format = '%B')
    # dob_d = DateField('Day', validators = [DataRequired(), NumberRange(min = 1, max = 31)], format = '%m')
    
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Passrowd', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # create a custom validation
    # check whether username exists already
    # def validate_name(self, name):
    #     user = User.query.filter_by(name = name.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one. ')
    
    # check whether email is already used
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one. ')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    # remember = BooleanField('Remember Me') 
    # we will remember user by default unless they sign out manually
    submit = SubmitField('Log In')