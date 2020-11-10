from flask import render_template, redirect, url_for, flash, request
from simulating_twitter import app, db, bcrypt
from simulating_twitter.models import User, Post
from simulating_twitter.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/', methods = ['GET', 'POST'])
def home_notauth():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if not form.validate() and form.is_submitted():
        flash('There was unusual login activity on your account. To help keep your account safe, \
            please enter your phone number or email address to verify it’s you.', 'warning')
        return redirect(url_for('login'))
    elif form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = True)
            return redirect(url_for('home'))
        else: 
            flash('Something went wrong.')
            return redirect(url_for('login'))
    
    return render_template('home_notauth.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        # if user exists & password correct 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log the user in with the flask extension
            login_user(user, remember = True)
            # using .get() instead of [] to get the dict value will avoid error from not having a value
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) # ternary conditional
        else:
            flash('There was unusual login activity on your account. To help keep your account safe, \
                    please enter your phone number or email address to verify it’s you.', 'warning')

    return render_template('login.html', form = form)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)


# this function doesn't take any args, because it already knew what user already logged in
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_notauth'))


# @app.rounte('/')
@app.route('/home')
@login_required
def home():
    image_file = url_for('static', filename = 'img/' + current_user.image_file)
    # .image_file is a column from the User model 
    return render_template('home.html', \
        posts = posts, image_file = image_file)


@app.route('/explore', methods = ['GET', 'POST'])
@login_required
def explore():
    return render_template('explore.html', trends = trends, happenings = happenings)


@app.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


@app.route('/notifications/mentions')
@login_required
def notifications_mentions():
    return render_template('notifications_mentions.html')


@app.route('/messages')
@login_required
def messages():
    return render_template('messages.html')


@app.route('/bookmarks')
@login_required
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/profile/lists')
@login_required
def profile_lists():
    return render_template('profile_lists.html')


@app.route('/lists/create')
@login_required
def lists_create():
    return render_template('lists_create.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile/with_replies')
@login_required
def profile_with_replies():
    return render_template('profile_with_replies.html')


@app.route('/profile/media')
@login_required
def profile_media():
    return render_template('profile_media.html')


@app.route('/profile/likes')
@login_required
def profile_likes():
    return render_template('profile_likes.html')


@app.route('/settings/profile')
@login_required
def settings_profile():
    return render_template('settings_profile.html')


@app.route('/compose/chirp')
@login_required
def compose_chirp():
    return render_template('compose_chirp.html')


@app.route('/account/add')
@login_required
def account_add():
    return render_template('account_add.html')


@app.route('/account/switch')
@login_required
def account_switch():
    return render_template('account_switch.html')


@app.route('/trends')
@login_required
def trends():
    return render_template('trends.html', \
        trends = trends)


@app.route('/timeline')
@login_required
def timeline():
    return render_template('timeline.html', \
        happenings = happenings)


@app.route('/connect_people')
@login_required
def connect_people():
    return render_template('connect_people.html')



posts = [
    {
        'icon': 'icon 1',
        'username': 'username 1',
        'handle': '@handle 1',
        'time': 'date 1',
        'content': 'content 1',
        'comment': 'comment button 1',
        'rechirp': 'rechirp button 1',
        'like': 'like button 1',
        'share': 'share buttton dropdown 1'
    },
    {
        'icon': 'icon 2',
        'username': 'username 2',
        'handle': '@handle 2',
        'time': 'date 2',
        'content': 'content 2',
        'comment': 'comment button 2',
        'rechirp': 'rechirp button 2',
        'like': 'like button 2',
        'share': 'share buttton dropdown 2'
    },
]

trends = [
    {
        'label': 'label 1',
        'topic': 'topic 1',
        'content': 'content 1',
        'chirp_count': 'count 1'
    },
    {
        'label': 'label 2',
        'topic': 'topic 2',
        'content': 'content 2',
        'chirp_count': 'count 2'
    }
]

happenings = [
    {
        'label': 'label 1',
        'time': 'time 1',
        'title': 'title 1'
    },
    {
        'label': 'label 2',
        'time': 'time 2',
        'title': 'title 2'
    }
]

people = [
    {   
        'icon': 'icon 1',
        'username': 'username 1',
        'handle': '@handle 1'
    },
    {
        'icon': 'icon 2',
        'username': 'username 2',
        'handle': '@handle 2'
    }
]