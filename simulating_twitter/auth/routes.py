import calendar
import datetime
from secrets import token_urlsafe
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user, login_required
from itsdangerous import NoneAlgorithm
from simulating_twitter import db, bcrypt
from simulating_twitter.models import User
from simulating_twitter.auth.forms import LoginForm, PersonalInfoForm, ChirperTrackerForm, \
    RegistrationForm, VerifyCodeForm, PasswordForm
from simulating_twitter.auth.utils import send_verification_email, verify_verification_code


auth = Blueprint('auth', __name__)

@auth.route('/', methods = ['GET', 'POST'])
def home_notauth():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if not form.validate() and form.is_submitted():
        flash('There was unusual login activity on your account. To help keep your account safe, \
            please enter your phone number or email address to verify it’s you.', 'warning')
        return redirect(url_for('auth.login'))
    elif form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = True)
            return redirect(url_for('main.home'))
        else: 
            flash('Something went wrong.')
            return redirect(url_for('auth.login'))
    
    return render_template('home_notauth.html', form = form)


# 
@auth.route('/signup/1', methods = ['GET', 'POST'])
def signup_1():
    form = PersonalInfoForm()
    if form.validate_on_submit():
        
        session['name'] = form.name.data
        session['email'] = form.email.data

        dob = form.dob_y.data + form.dob_m.data + form.dob_d.data
        session['dob'] = datetime.datetime.strptime(dob, '%Y%B%d')
        
        return redirect(url_for('auth.signup_2'))
    return render_template('signup_1.html', form = form)


# 
@auth.route('/signup/2', methods = ['GET', 'POST'])
def signup_2():
    if request.referrer is None:
        return redirect(url_for('auth.signup_1'))

    form = ChirperTrackerForm()
    if form.validate_on_submit():
        session['tracker'] = form.tracker.data
        return redirect(url_for('auth.signup_3'))

    return render_template('signup_2.html', form = form)


# 
@auth.route('/signup/3', methods = ['GET', 'POST'])
def signup_3():
    if request.referrer is None:
        return redirect(url_for('auth.signup_1'))

    form = RegistrationForm()
    birthdate = session.get('dob').strftime('%b %d, %Y')
    email = session.get('email')
    if request.method == 'GET':
        form.name.data = session.get('name')

    elif request.method == 'POST':
        # can't use .validate_on_submit() because not all fields are plugged in
        if form.is_submitted():
            send_verification_email(session.get('email'))
            return redirect(url_for('auth.signup_4'))

    return render_template('signup_3.html', form = form, birthdate = birthdate, email = email)


# 
@auth.route('/signup/4', methods = ['GET', 'POST'])
def signup_4():
    if request.referrer is None:
        return redirect(url_for('auth.signup_1'))

    form = VerifyCodeForm()

    if form.validate_on_submit():
        if not verify_verification_code(form.code.data):
            flash('Incorrect code. Please try again.')
        else:
            return redirect(url_for('auth.signup_5'))

    return render_template('signup_4.html', form = form)
   

# 
@auth.route('/signup/5', methods = ['GET', 'POST'])
def signup_5():
    if request.referrer is None:
        return redirect(url_for('auth.signup_1'))

    form = PasswordForm()
    if form.validate_on_submit():
        # generate a random url/handle for the user, check if duplicate in the db
        handle = token_urlsafe(5)
        if handle == User.query.filter_by(handle = handle).first():
            handle = token_urlsafe(5)

        user = User(name = session.get('name'), email = session.get('email'), \
        birthdate = session.get('dob'), \
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'), \
        handle = handle, created_at_ip = request.remote_addr)

        db.session.add(user)
        db.session.commit()

        session.pop('name')
        session.pop('email')
        session.pop('dob')
        session.pop('tracker')

        login_user(user)

        return redirect(url_for('user.profile', handle = current_user.handle))
    return render_template('signup_5.html', form = form)

    
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        # if user exists & password correct 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log the user in with the flask extension
            login_user(user, remember = True)
            # using .get() instead of [] to get the dict value will avoid error from not having a value
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home')) # ternary conditional
        else:
            flash('There was unusual login activity on your account. To help keep your account safe, \
                    please enter your phone number or email address to verify it’s you.', 'warning')

    return render_template('login.html', form = form)


# this function doesn't take any args, because it already knew what user already logged in
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.home_notauth'))


@auth.route('/account/add')
@login_required
def account_add():
    profile_image = url_for('static', filename = 'img/profile_pics/' + current_user.profile_image)
    return render_template('account_add.html', profile_image = profile_image)


@auth.route('/account/switch')
@login_required
def account_switch():
    profile_image = url_for('static', filename = 'img/profile_pics/' + current_user.profile_image)
    return render_template('account_switch.html', profile_image = profile_image)