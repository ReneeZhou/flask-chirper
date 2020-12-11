from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from simulating_twitter import db, bcrypt
from simulating_twitter.models import User
from simulating_twitter.account.forms import BeginPasswordResetForm, SendPasswordResetForm, \
    ConfirmPinResetForm, ResetPasswordForm, PasswordResetSurveyForm
from simulating_twitter.account.utils import send_pin_email


account = Blueprint('account', __name__)
# __name__ is showing you the current file name
# whether that be __main__ (run directly) or .py name (run indirectly)
# we are importing from this users package itself


@account.route('/account/begin_password_reset', methods = ['GET', 'POST'])
def account_beginPasswordReset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        session['email'] = request.form['email']
        return redirect(url_for('account.account_sendPasswordReset'))

    return render_template('account_beginPasswordReset.html', form = form)


@account.route('/account/send_password_reset', methods = ['GET', 'POST'])
def account_sendPasswordReset():
    # not allowing request from outside a URL
    if request.referrer is None:
        session['email'] = ''
        # if session.pop('email') would raise a keyError
        return redirect(url_for('account.account_beginPasswordReset'))

    form = SendPasswordResetForm()
    user = User.query.filter_by(email = session.get('email')).first()
    if form.validate_on_submit():
        send_pin_email(user)
        return redirect(url_for('account.account_confirmPinReset'))
    
    return render_template('account_sendPasswordReset.html', form = form, user = user)


@account.route('/account/confirm_pin_reset', methods = ['GET', 'POST'])
def account_confirmPinReset():
    if request.referrer is None:
        session['email'] = ''
        return redirect(url_for('account.account_beginPasswordReset'))

    form = ConfirmPinResetForm()
    
    if form.pin.data is not None:
        user = User.verify_reset_token(form.pin.data)
        if user is None: 
            flash('Incorrect code. Please try again.', 'warning')

        elif form.validate_on_submit():
            return redirect(url_for('account.account_resetPassword'))
        # implement something for 'didn't receive your code'
        # and will resend a token

    return render_template('account_confirmPinReset.html', form = form)


@account.route('/account/reset_password', methods = ['GET', 'POST'])
def account_resetPassword():
    if request.referrer is None:
        session['email'] = ''
        return redirect(url_for('account.account_beginPasswordReset'))

    form = ResetPasswordForm()
    user = User.query.filter_by(email = session.get('email')).first()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('account.account_passwordResetSurvey'))

    return render_template('account_resetPassword.html', form = form, user = user)


@account.route('/account/password_reset_survey', methods = ['GET', 'POST'])
def account_passwordResetSurvey():
    if request.referrer is None:
        session['email'] = ''
        return redirect(url_for('account.account_beginPasswordReset'))

    form = PasswordResetSurveyForm()
    if form.validate_on_submit():
        return redirect(url_for('account.account_passwordResetComplete'))
    return render_template('account_passwordResetSurvey.html', form = form)


@account.route('/account/password_reset_complete')
def account_passwordResetComplete():
    if request.referrer is None:
        session['email'] = ''
        return redirect(url_for('account.account_beginPasswordReset'))

    return render_template('account_passwordResetComplete.html')