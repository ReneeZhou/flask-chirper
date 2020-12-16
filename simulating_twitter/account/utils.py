from flask import render_template
from flask_mail import Message
from simulating_twitter import mail


def send_pin_email(user):
    pin = user.get_reset_token()
    msg = Message('Password reset request', \
        sender = 'reneezsr@gmail.com ', \
        recipients = [user.email], \
        html = render_template('mail_passwordResetRequest.html', \
            pin = pin, handle = user.handle))    # user.email
    mail.send(msg)