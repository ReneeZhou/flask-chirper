from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # FileAllowed is a validator restricting file type
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeField    # BooleanField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from simulating_twitter.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(max = 50)])
    email = EmailField('Email', validators = [DataRequired(), Email()])
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


class PostForm(FlaskForm):
    dated_posted = DateTimeField('Timestamp', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired(), Length(max = 280)])
    user_id = StringField('UserId', validators = [DataRequired()])
    submit = SubmitField('Chirp')