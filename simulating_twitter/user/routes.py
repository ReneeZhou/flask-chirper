from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from simulating_twitter import db
from simulating_twitter.models import User, Post
from simulating_twitter.post.utils import show_time
from simulating_twitter.main.utils import get_recommendation


user = Blueprint('user', __name__)

@user.route('/<handle>')
def profile(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    posts = Post.query.filter_by(user_id = user.id).order_by(Post.created_at.desc()).all()
    for post in posts:
        post.show = show_time(post.created_at)
    posts_num = len(posts)

    if current_user.is_authenticated:
        following_status = current_user.is_following(user)
        follow_recommendation = get_recommendation(current_user)
    else: 
        following_status = None
        follow_recommendation = None

    return render_template('profile.html', user = user, posts = posts, posts_num = posts_num, \
        following_status = following_status, follow_recommendation = follow_recommendation)


@user.route('/<handle>/with_replies')
def profile_with_replies(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    if current_user.is_authenticated:
        follow_recommendation = get_recommendation(current_user)
    else:
        follow_recommendation = None

    return render_template('profile_with_replies.html', user = user, follow_recommendation = follow_recommendation)


@user.route('/<handle>/media')
def profile_media(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    if not current_user.is_authenticated:
        return redirect(url_for('user.profile', handle = user.handle))
    
    if current_user.is_authenticated:
        follow_recommendation = get_recommendation(current_user)
        
    return render_template('profile_media.html', user = user, follow_recommendation = follow_recommendation)


@user.route('/<handle>/likes')
def profile_likes(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    if not current_user.is_authenticated:
        return redirect(url_for('user.profile', handle = user.handle))

    if current_user.is_authenticated:
        follow_recommendation = get_recommendation(current_user)

    return render_template('profile_likes.html', user = user, follow_recommendation = follow_recommendation)


# needs fixing <handle>
@user.route('/profile/lists')
@login_required
def profile_lists():
    follow_recommendation = get_recommendation(current_user)
    return render_template('profile_lists.html', follow_recommendation = follow_recommendation)


@user.route('/<handle>/moments')
def profile_moments(handle):
    return render_template('profile_moments.html')


@user.route('/<handle>/topics')
def profile_topics(handle):
    return render_template('profile_topics.html')


@user.route('/<handle>/follow', methods = ['POST'])
@login_required
def follow(handle):
    user = User.query.filter_by(handle = handle).first_or_404()
    
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('user.profile', handle = user.handle))


@user.route('/<handle>/unfollow', methods = ['POST'])
@login_required
def unfollow(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('user.profile', handle = user.handle))