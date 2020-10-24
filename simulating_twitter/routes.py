from flask import render_template, redirect, url_for
from simulating_twitter import app
from simulating_twitter.models import User, Post
from simulating_twitter.forms import LoginForm, RegistrationForm

@app.route('/')
def home_notauth():
    return render_template('home_notauth.html')


# @app.rounte('/')
@app.route('/home')
def home():
    return render_template('home.html', \
        posts = posts, trends = trends, people = people)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = RegistrationForm()
    return render_template('signup.html', form = form)


@app.route('/explore')
def explore():
    return render_template('explore.html', trends = trends, happenings = happenings)



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



posts = [
    {
        'icon': 'icon 1',
        'username': 'username 1',
        'handle': '@handle 1',
        'time': 'date 1',
        'content': 'content 1',
        'comment': 'comment button 1',
        'retweet': 'retweet button 1',
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
        'retweet': 'retweet button 2',
        'like': 'like button 2',
        'share': 'share buttton dropdown 2'
    },
]

trends = [
    {
        'label': 'label 1',
        'topic': 'topic 1',
        'content': 'content 1',
        'tweet_count': 'count 1'
    },
    {
        'label': 'label 2',
        'topic': 'topic 2',
        'content': 'content 2',
        'tweet_count': 'count 2'
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