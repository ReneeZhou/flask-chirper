from secrets import randbits
from datetime import datetime
from flask import render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_required
from simulating_twitter import db
from simulating_twitter.models import User, Post, follower, Message
from simulating_twitter.main.forms import MessageForm
from simulating_twitter.post.forms import PostForm


main = Blueprint('main', __name__)

@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(id = randbits(60), content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('home.html', form = form)


@main.route('/explore', methods = ['GET', 'POST'])
def explore():
    return render_template('explore.html', trends = trends, happenings = happenings)


@main.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')


@main.route('/notifications/mentions')
@login_required
def notifications_mentions():
    return render_template('notifications_mentions.html')


@main.route('/messages')
@login_required
def messages():
    current_user.last_read_message_at = datetime.utcnow()
    db.session.commit()
    
    return render_template('messages.html')


@main.route('/messages/compose')
@login_required
def messages_compose():
    return render_template('messages_compose.html')


@main.route('/messages/<int:counterpart_id>-<int:currentuser_id>', methods = ['GET', 'POST'])
@login_required
def messages_counterpart(counterpart_id, currentuser_id):
    if currentuser_id != current_user.id or User.query.get(counterpart_id) is None: 
        return redirect(url_for('main.messages'))

    counterpart = User.query.get(counterpart_id)

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(id = randbits(60), sender_id = current_user.id, \
            recipient_id = counterpart.id, body = form.message.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('main.messages_counterpart', \
            counterpart_id = counterpart_id, currentuser_id = current_user.id))
    
    message_history = current_user.messages_received.filter_by(
        sender_id = counterpart.id).union(current_user.messages_sent.filter_by(
            recipient_id = counterpart_id)).order_by(Message.created_at)

    return render_template('messages_counterpart.html', form = form, \
        counterpart_id = counterpart_id, currentuser_id = currentuser_id, counterpart = counterpart, \
            message_history = message_history)


@main.route('/messages/<int:counterpart_id>-<int:currentuser_id>/info')
@login_required
def messages_counterpart_info(counterpart_id, currentuser_id):
    if currentuser_id != current_user.id or User.query.get(counterpart_id) is None: 
        return redirect(url_for('main.messages'))

    counterpart = User.query.get(counterpart_id)

    return render_template('messages_counterpart_info.html', \
        counterpart_id = counterpart_id, currentuser_id = currentuser_id, \
        counterpart = counterpart)


@main.route('/follower_requests')
@login_required
def followerRequests():
    return render_template('followerRequests.html')


# i
@main.route('/bookmarks')
@login_required
def bookmarks():
    return render_template('bookmarks.html')


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
    return render_template('trends.html', trends = trends)


# i
@main.route('/timeline')
@login_required
def timeline():
    return render_template('timeline.html', happenings = happenings)


# i
@main.route('/connectPeople')
@login_required
def connectPeople():
    return render_template('connectPeople.html')


# i
@main.route('/display')
def display():
    return render_template('display.html')


# i
@main.route('/keyboard_shortcuts')
def keyboardShortcuts():
    return render_template('keyboardShortcuts.html')




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