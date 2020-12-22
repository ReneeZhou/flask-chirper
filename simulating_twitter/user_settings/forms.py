from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
from simulating_twitter.models import User



class UpdateProfileForm(FlaskForm):
    # profile & background pic
    profile_image = FileField('Update profile picture', validators = [FileAllowed(['jpg', 'png'])])
    background_image = FileField('Update background image', validators = [FileAllowed(['jpg', 'png'])])

    # these 4 fields don't have to be unique
    name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
    bio = TextAreaField('Bio', validators = [Length(max = 160)])
    location = StringField('Location', validators = [Length(max = 30)])
    website = URLField('Website', validators = [Length(max = 100)])
    submit = SubmitField('Save')


class UpdateAccountForm(FlaskForm): 
    handle = StringField('Handle', validators = [DataRequired()])
    email = EmailField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_handle(self, handle):
        if handle.data != current_user.handle:
            user = User.query.filter_by(handle = handle.data).first()
            if user:
                raise ValidationError('This handle has been taken. It\'s an unique identifier. \
                    You must choose something else.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email has been taken. Please choose another one.')


class ConfirmPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Confirm')


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators = [DataRequired()])
    new_password = PasswordField('New password', validators = [DataRequired(), \
        Length(min = 8, message = 'Your password needs to be at least 8 characters. Please enter a long one.')])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), \
        EqualTo('new_password', 'Passwords do not match.')])
    submit = SubmitField('Save')


class UpdateScreenNameForm(FlaskForm):
    screen_name = StringField('Username', validators = [DataRequired()])
    submit = SubmitField('Save')

    def validate_screen_name(self, screen_name):
        user = User.query.filter_by(handle = screen_name.data).first()
        if user:
            raise ValidationError('That username has been taken. Please choose another.')