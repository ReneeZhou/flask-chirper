from simulating_twitter import app
from flask import render_template, redirect

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')



@app.route('/notifications')
def notifications():
    return render_template('notifications.html')



@app.route('/messages')
def messages():
    return render_template('messages.html')



@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')



@app.route('/profile/lists')
def lists():
    return render_template('lists.html')



@app.route('/profile')
def profile():
    return render_template('profile.html')



@app.route('/compose/tweet')
def tweet():
    return render_template('tweet.html')


@app.route('/account/add')
def account_add():
    return render_template('account_add.html')


@app.route('/account/switch')
def account_switch():
    return render_template('account_switch.html')