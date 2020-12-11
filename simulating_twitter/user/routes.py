from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from simulating_twitter.models import User, Post
from simulating_twitter.post.utils import show_time


user = Blueprint('user', __name__)

@user.route('/<handle>')
def profile(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    posts = Post.query.filter_by(user_id = user.id).order_by(Post.date_posted.desc()).all()
    for post in posts:
        post.show = show_time(post.date_posted)
    posts_num = len(posts)

    return render_template('profile.html', user = user, posts = posts, posts_num = posts_num)


@user.route('/<handle>/with_replies')
def profile_with_replies(handle):
    user = User.query.filter_by(handle = handle).first_or_404()
    return render_template('profile_with_replies.html', user = user)


@user.route('/<handle>/media')
def profile_media(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    if not current_user.is_authenticated:
        return redirect(url_for('user.profile', handle = user.handle))

    return render_template('profile_media.html', user = user)


@user.route('/<handle>/likes')
def profile_likes(handle):
    user = User.query.filter_by(handle = handle).first_or_404()

    if not current_user.is_authenticated:
        return redirect(url_for('user.profile', handle = user.handle))

    return render_template('profile_likes.html', user = user)


# needs fixing <handle>
@user.route('/profile/lists')
@login_required
def profile_lists():
    return render_template('profile_lists.html')


@user.route('/<handle>/moments')
def profile_moments(handle):
    return render_template('profile_moments.html')


@user.route('/<handle>/topics')
def profile_topics(handle):
    return render_template('profile_topics.html')