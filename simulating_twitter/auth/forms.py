import calendar
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from simulating_twitter.models import User



class PersonalInfoForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
    email = EmailField('Email', validators = [DataRequired(), Email()])


    year = [i for i in range(1900, datetime.datetime.utcnow().year + 1)][::-1]
    month = [i for i in calendar.month_name][1:]
    day = [i for i in range(1, 32)]


    dob_y = SelectField('Year', validators = [DataRequired()], choices = year)
    dob_m = SelectField('Month', validators = [DataRequired()], choices = month)
    dob_d = SelectField('Day', validators = [DataRequired()], choices = day)

    submit = SubmitField('Next')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


    def validate_dob_d(self, dob_d):
        if self.dob_m.data == 'February':
            if int(dob_d.data) > 29:
                raise ValidationError('Invalid date. Please reselect.')
            elif int(dob_d.data) == 29:
                if not calendar.isleap(int(self.dob_y.data)):
                    raise ValidationError('Invalid date. Please reselect.')
        elif self.dob_m.data in ['April', 'June', 'September', 'November']:
            if int(dob_d.data) > 30:
                raise ValidationError('Invalid date. Please reselect.')
        
   

class ChirperTrackerForm(FlaskForm):
    tracker = BooleanField('Chirper uses this data to personalize your experience.\
        This web browsing history will never be stored with your name, email, or phone number.', \
            default = "checked")
    submit = SubmitField('Next')



class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
    email = EmailField('Email', validators = [DataRequired(), Email()])
    birthdate = StringField('Birth date', validators = [DataRequired()])
    submit = SubmitField('Sign up')


class VerifyCodeForm(FlaskForm):
    code = StringField('Verification code', validators = [DataRequired(), Length(max = 200)])
    submit = SubmitField('Next')


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired(), \
        Length(min = 8, message = 'Your password needs to be at least 8 characters. Please enter a long one.')])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message = 'Passwords do not match.')])
    submit = SubmitField('Next')


# class RegistrationForm1(FlaskForm):
#     name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
#     email = EmailField('Email', validators = [DataRequired(), Email()])
    
#     # dob_y = DateField('Year', validators = [DataRequired(), NumberRange(min = 1990, max = datetime.utcnow().year)], format = '%Y')
#     # dob_m = DateField('Month', validators = [DataRequired(), NumberRange(min = 1, max = 12)], format = '%B')
#     # dob_d = DateField('Day', validators = [DataRequired(), NumberRange(min = 1, max = 31)], format = '%m')
    
#     password = PasswordField('Password', validators = [DataRequired(), \
#         Length(min = 8, message = 'Your password needs to be at least 8 characters. Please enter a long one.')])
#     confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')

#     # create a custom validation
#     # check whether username exists already
#     # def validate_name(self, name):
#     #     user = User.query.filter_by(name = name.data).first()
#     #     if user:
#     #         raise ValidationError('That username is taken. Please choose a different one. ')
    
#     # check whether email is already used
#     def validate_email(self, email):
#         user = User.query.filter_by(email = email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one. ')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    # remember = BooleanField('Remember Me') 
    # we will remember user by default unless they sign out manually
    submit = SubmitField('Log In')