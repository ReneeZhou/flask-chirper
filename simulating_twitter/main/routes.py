from secrets import randbits
from datetime import datetime
from flask import render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_required
from simulating_twitter import db
from simulating_twitter.models import User, Post, follower, Message
from simulating_twitter.main.utils import get_recommendation
from simulating_twitter.main.forms import MessageForm
from simulating_twitter.post.utils import show_time
from simulating_twitter.post.forms import PostForm


main = Blueprint('main', __name__)

@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post_id = randbits(60), content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))

    # posts = Post.query.order_by(Post.created_at.desc()).all()
    posts = current_user.following_post().all()

    for post in posts:
        post.show = show_time(post.created_at)
    # .profile_image is a column from the User model 

    follow_recommendation = get_recommendation(current_user)

    return render_template('home.html', form = form, posts = posts, follow_recommendation = follow_recommendation)


@main.route('/explore', methods = ['GET', 'POST'])
def explore():
    follow_recommendation = get_recommendation(current_user)
    return render_template('explore.html', trends = trends, happenings = happenings, follow_recommendation = follow_recommendation)


@main.route('/notifications')
@login_required
def notifications():
    follow_recommendation = get_recommendation(current_user)
    return render_template('notifications.html', follow_recommendation = follow_recommendation)


@main.route('/notifications/mentions')
@login_required
def notifications_mentions():
    follow_recommendation = get_recommendation(current_user)
    return render_template('notifications_mentions.html', follow_recommendation = follow_recommendation)


@main.route('/messages')
@login_required
def messages():
    following_users = current_user.following.filter(follower.c.follower_id == current_user.id).all()
    return render_template('messages.html', following_users = following_users)


@main.route('/messages/compose')
@login_required
def messages_compose():
    following_users = current_user.following.filter(follower.c.follower_id == current_user.id).all()
    return render_template('messages_compose.html', following_users = following_users)


@main.route('/messages/<int:counterpart_id>-<int:currentuser_id>', methods = ['GET', 'POST'])
def messages_counterpart(counterpart_id, currentuser_id):
    if currentuser_id != current_user.id or User.query.get(counterpart_id) is None: 
        return redirect(url_for('main.messages'))

    following_users = current_user.following.filter(follower.c.follower_id == current_user.id).all()
    counterpart = User.query.get(counterpart_id)

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(id = randbits(60), sender_id = current_user.id, \
            recipient_id = counterpart.id, body = form.message.data)
        db.session.add(message)
        db.session.commit()
    

    current_user.last_read_message_at = datetime.utcnow()
    db.session.commit()
    
    message_history = current_user.message_received.filter_by(
        sender_id = counterpart.id).union(current_user.message_sent.filter_by(
            recipient_id = counterpart_id)).order_by(Message.created_at)
        
        # filter_by(
        #     sender_id = (current_user.id or counterpart.id)).filter_by(
        #         recipient_id = (current_user.id or counterpart.id)).all()


    return render_template('messages_counterpart.html', form = form, following_users = following_users, \
        counterpart_id = counterpart_id, currentuser_id = currentuser_id, counterpart = counterpart, \
            message_history = message_history)


@main.route('/follower_requests')
def followerRequests():
    return render_template('followerRequests.html')


# i
@main.route('/bookmarks')
@login_required
def bookmarks():
    follow_recommendation = get_recommendation(current_user)
    return render_template('bookmarks.html', follow_recommendation = follow_recommendation)


# i
@main.route('/lists/create')
@login_required
def lists_create():
    return render_template('lists_create.html')


# i
@main.route('/lists/add_member')
@login_required
def lists_addMember():
    return render_template('lists_addMember.html')


# i
@main.route('/trends')
@login_required
def trends():
    follow_recommendation = get_recommendation(current_user)
    return render_template('trends.html', trends = trends, follow_recommendation = follow_recommendation)


# i
@main.route('/timeline')
@login_required
def timeline():
    follow_recommendation = get_recommendation(current_user)
    return render_template('timeline.html', happenings = happenings, follow_recommendation = follow_recommendation)


# i
@main.route('/connect_people')
@login_required
def connect_people():
    return render_template('connect_people.html')


# i
@main.route('/display')
def display():
    return render_template('display.html')


# i
@main.route('/keyboard_shortcuts')
def keyboardShortcuts():
    return render_template('keyboardShortcuts.html')





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