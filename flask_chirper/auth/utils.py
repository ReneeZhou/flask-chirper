from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import render_template, current_app
from flask_mail import Message
from flask_chirper import mail



def get_verification_code(email, expires_sec = 300):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in = expires_sec)
    return s.dumps({'email': email}).decode('utf-8')


def send_verification_email(email):
    pin = get_verification_code(email)
    msg = Message(
        subject = 'Your email registration code.', \
        sender = 'reneezsr@gmail.com', \
        recipients = [email], \
        html = render_template('mail_registrationVerification.html', pin = pin))
    mail.send(msg)


def verify_verification_code(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token)['email']
        return email
    except:
        return None
