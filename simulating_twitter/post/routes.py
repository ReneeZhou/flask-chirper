from secrets import randbits
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from simulating_twitter import db
from simulating_twitter.models import Post
from simulating_twitter.post.forms import PostForm


post = Blueprint('post', __name__)

@post.route('/<handle>/status/<int:post_id>', methods = ['GET', 'POST'])
def status(handle, post_id):
    post = Post.query.get_or_404(post_id)
    
    if handle != post.author.handle:
        handle = post.author.handle
        post_id = post.post_id
        return redirect(url_for('post.status', handle = handle, post_id = post_id))
    
    return render_template('status.html', post = post)


@post.route('/<handle>/status/<int:post_id>/analytics', methods = ['GET'])
@login_required
def status_analytics(handle, post_id):
    post = Post.query.get_or_404(post_id)

    if handle != post.author.handle:
        handle = post.author.handle
        post_id = post.post_id
        return redirect(url_for('post.status_analytics', handle = handle, post_id = post_id))

    return render_template('status_analytics.html', post = post)


@post.route('/<handle>/status/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_chirp(handle, post_id):
    post = Post.query.get_or_404(post_id)

    if handle != post.author.handle:
        handle = post.author.handle
        post_id = post.post_id
        return redirect(url_for('post.status', handle = handle, post_id = post_id))

    # route forbidded if it's not post owner
    if post.author != current_user:
        abort(403)

    # pre-fill content
    form = PostForm()
    if request.method == 'GET':
        form.content.data = post.content
    
    if form.validate_on_submit():
        post.content = form.content.data
        # post.date_posted = datetime.utcnow()  optional
        db.session.commit()
        # flash('Your chirp has been updated. ', 'success')
        return redirect(url_for('post.status', handle = handle, post_id = post.post_id))

    return render_template('status_update.html', post = post, form = form)


@post.route('/<handle>/status/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_chirp(handle, post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your chirp was deleted', 'success')
    return redirect(url_for('user.profile', handle = current_user.handle))


@post.route('/compose/chirp', methods = ['GET', 'POST'])
@login_required
def compose_chirp():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post_id = randbits(60), content = form.content.data, author = current_user)  # from the backref in db
        db.session.add(post)
        db.session.commit()
        flash('Your Chirp was sent. View')
        return redirect(url_for('user.profile', handle = current_user.handle))
    return render_template('compose_chirp.html', form = form)