from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from simulating_twitter.models import User


class BeginPasswordResetForm(FlaskForm):
    email = EmailField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Search')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("We couldn't find your account with that information.")


class SendPasswordResetForm(FlaskForm):
    information = RadioField('You can use the information associated with your account', \
        validators = [DataRequired()], \
        choices = [('Email', 'Send an email to')], default = "Email")
            # ('Phone', 'Text a code to the phone number ending in')
            # to generate the dynamic list, check wtf doc
            # do it in in the view function
    submit = SubmitField('Next')


class ConfirmPinResetForm(FlaskForm):
    pin = StringField('Pin', validators = [DataRequired()])
    submit = SubmitField('Verify')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter your new password', validators = [DataRequired()])
    confirm_password = PasswordField('Enter your password one more time', \
        validators = [DataRequired(), EqualTo('password', message = 'Passwords do not match.')])
    remember = BooleanField('Remember me', default = "checked")
    # this might currently serve any purpose as our default is remembering user's login
    # until they manually log out
    submit = SubmitField('Reset password')


class PasswordResetSurveyForm(FlaskForm):
    reasons = RadioField('Reasons', \
        choices = ['Forgot password', 'Account may have been accessed by someone else', 'Another reason'])
    submit = SubmitField('Submit')