import os
from datetime import datetime
from secrets import token_urlsafe, token_hex
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from sqlalchemy.sql.visitors import replacement_traverse
from werkzeug.utils import validate_arguments
from simulating_twitter import app, db, bcrypt
from simulating_twitter.models import User, Post
from simulating_twitter.forms import LoginForm, PostForm, RegistrationForm, UpdateProfileForm, UpdateAccountForm
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
            login_user(user) # , remember = True)
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
            login_user(user) # , remember = True)
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

        # generate a random url/handle for the user, check if duplicate in the db
        handle = token_urlsafe(5)
        if handle == User.query.filter_by(handle = handle).first():
            handle = token_urlsafe(5)

        user = User(handle = handle, name = form.name.data, email = form.email.data, password = hashed_password)
            # dob_y = form.dob_y.data, dob_m = form.dob_m.data, dob_d = form.dob_d.data)
        
        # user = User(username = form.username.data, email = form.email.data, password = hashed_password)
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


def show_time(date_posted):
    t = datetime.utcnow() - date_posted
    if t.seconds < 59:
        return f'{t.seconds}s'
    elif 50 <= t.seconds < 3600:
        return f'{t.seconds//60}m'
    elif t.days < 1:
        return f'{t.seconds//3600}h'
    elif date_posted.year == datetime.utcnow().year:
        return date_posted.strftime('%d %b')
    else: 
        return date_posted.strftime('%d %b %Y')


@app.route('/profile/status/<int:post_id>')
def status(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('status.html', post = post, post_id = post_id)


@app.route('/profile/status/<int:post_id>/update', methods = ['GET', 'POST'])
def update_chirp(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    if request.method == 'GET':
        form.content.data = post.content
    
    if form.validate_on_submit():
        post.content = form.content.data
        # post.date_posted = datetime.utcnow()  optional
        db.session.commit()
        # flash('Your chirp has been updated. ', 'success')
        return redirect(url_for('status', post_id = post_id))

    return render_template('status_update.html', post = post, form = form)


@app.errorhandler(404)
@login_required
def page_not_found(error_status):
    return render_template('404.html', error_status = 404)


# @app.rounte('/')
@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    posts = Post.query.all()
    for post in posts:
        post.show = show_time(post.date_posted)
    # .profile_image is a column from the User model 
    return render_template('home.html', form = form, posts = posts)


@app.route('/explore', methods = ['GET', 'POST'])
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


@app.route('/<handle>')
def profile(handle):
    user = User.query.filter_by(handle = handle).first()
    return render_template('profile.html', user = user)


@app.route('/<handle>/with_replies')
def profile_with_replies(handle):
    user = User.query.filter_by(handle = handle).first()
    return render_template('profile_with_replies.html', user = user)


@app.route('/<handle>/media')
def profile_media(handle):
    user = User.query.filter_by(handle = handle).first()

    if not current_user.is_authenticated:
        return redirect(url_for('profile', handle = user.handle))

    return render_template('profile_media.html', user = user)


@app.route('/<handle>/likes')
def profile_likes(handle):
    user = User.query.filter_by(handle = handle).first()

    if not current_user.is_authenticated:
        return redirect(url_for('profile', handle = user.handle))
        
    return render_template('profile_likes.html', user = user)


def save_image(form_image):
    # ramdonize user's image name so they don't collide in db
    random_hex = token_hex(8)
    # save the file with the same extension as user uploaded
    # if it's a file it will have this .filename attr from the form
    # throow away the first variable (f_name) because we won't need it 
    _, f_ext = os.path.splitext(form_image.filename)  
    picture_fn = random_hex + f_ext

    output_size = {'profile': (400, 400), 'background': (600, 200)}
    i = Image.open(form_image)

    if form_image.name == 'profile_image':
        picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
        i.thumbnail(output_size['profile'])
    elif form_image.name == 'background_image':
        picture_path = os.path.join(app.root_path, 'static/img/background_pics', picture_fn)
        i.thumbnail(output_size['background'])
    
    i.save(picture_path)

    return picture_fn


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings/profile', methods = ['GET', 'POST'])
@login_required
def settings_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.background_image.data: 
            current_user.background_image  = save_image(form.background_image.data)

        if form.profile_image.data:
            current_user.profile_image = save_image(form.profile_image.data)

        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', handle = current_user.handle))
        # POST/GET redirect pattern
        # browser telling you're about to run another POST when you reload your page
        # so us redirecting causing the browser to send a GET, and we won't get that pop up msg from browser
    
    # populate the form fields with existing user data
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website

    if current_user.background_image == None:
        background_image = None
    elif current_user.background_image:
        background_image = url_for('static', filename = 'img/background_pics/' + current_user.background_image)
    return render_template('settings_profile.html', form = form, background_image = background_image)


@app.route('/settings/account', methods = ['GET', 'POST'])
@login_required
def settings_account():
    form = UpdateAccountForm()

    if request.method == 'GET':
        form.handle.data = current_user.handle
        form.email.data = current_user.email

    elif form.validate_on_submit():
        if form.handle.data != current_user.handle or form.email.data != current_user.email: 
            current_user.handle = form.handle.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')    
        # needs fixing, it flashes when return to this page
        # return redirect(url_for('profile'))

    return render_template('settings_account.html', form = form)


@app.route('/compose/chirp', methods = ['GET', 'POST'])
@login_required
def compose_chirp():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content = form.content.data, author = current_user)  # from the backref in db
        db.session.add(post)
        db.session.commit()
        flash('Your Chirp was sent. View')
        # return redirect(url_for('profile'))
    return render_template('compose_chirp.html', form = form)


@app.route('/account/add')
@login_required
def account_add():
    profile_image = url_for('static', filename = 'img/profile_pics/' + current_user.profile_image)
    return render_template('account_add.html', profile_image = profile_image)


@app.route('/account/switch')
@login_required
def account_switch():
    profile_image = url_for('static', filename = 'img/profile_pics/' + current_user.profile_image)
    return render_template('account_switch.html', profile_image = profile_image)


@app.route('/trends')
@login_required
def trends():
    return render_template('trends.html', trends = trends)


@app.route('/timeline')
@login_required
def timeline():
    return render_template('timeline.html', happenings = happenings)


@app.route('/connect_people')
@login_required
def connect_people():
    return render_template('connect_people.html')



# posts = [
#     {
#         'icon': 'icon 1',
#         'username': 'username 1',
#         'handle': '@handle 1',
#         'time': 'date 1',
#         'content': 'content 1',
#         'comment': 'comment button 1',
#         'rechirp': 'rechirp button 1',
#         'like': 'like button 1',
#         'share': 'share buttton dropdown 1'
#     },
#     {
#         'icon': 'icon 2',
#         'username': 'username 2',
#         'handle': '@handle 2',
#         'time': 'date 2',
#         'content': 'content 2',
#         'comment': 'comment button 2',
#         'rechirp': 'rechirp button 2',
#         'like': 'like button 2',
#         'share': 'share buttton dropdown 2'
#     },
# ]

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