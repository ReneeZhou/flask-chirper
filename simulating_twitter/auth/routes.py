from secrets import token_urlsafe
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from simulating_twitter import db, bcrypt
from simulating_twitter.models import User
from simulating_twitter.auth.forms import LoginForm, RegistrationForm


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


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # generate a random url/handle for the user, check if duplicate in the db
        handle = token_urlsafe(5)
        if handle == User.query.filter_by(handle = handle).first():
            handle = token_urlsafe(5)

        user = User(handle = handle, name = form.name.data, email = form.email.data, password = hashed_password,\
            created_at_ip = request.remote_addr)
            # dob_y = form.dob_y.data, dob_m = form.dob_m.data, dob_d = form.dob_d.data)
        
        # user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form = form)


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