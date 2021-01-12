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
        post_id = post.id
        return redirect(url_for('post.status', handle = handle, post_id = post_id))
    
    return render_template('status.html', post = post)


@post.route('/<handle>/status/<int:post_id>/analytics', methods = ['GET'])
@login_required
def status_analytics(handle, post_id):
    post = Post.query.get_or_404(post_id)

    if handle != post.author.handle:
        handle = post.author.handle
        post_id = post.id
        return redirect(url_for('post.status_analytics', handle = handle, post_id = post_id))

    return render_template('status_analytics.html', post = post)


@post.route('/<handle>/status/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_chirp(handle, post_id):
    post = Post.query.get_or_404(post_id)

    if handle != post.author.handle:
        handle = post.author.handle
        post_id = post.id
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
        # post.created_at = datetime.utcnow()  optional
        db.session.commit()
        # flash('Your chirp has been updated. ', 'success')
        return redirect(url_for('post.status', handle = handle, post_id = post.id))

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


@post.route('/<handle>/status/<int:post_id>/like', methods = ['POST'])
@login_required
def like_chirp(handle, post_id):
    post = Post.query.get(post_id)
    
    current_user.liking(post)
    db.session.commit()

    return redirect(url_for('main.home'))


@post.route('/<handle>/status/<int:post_id>/unlike', methods = ['POST'])
@login_required
def unlike_chirp(handle, post_id):
    post = Post.query.get(post_id)

    current_user.unliking(post)
    db.session.commit()

    return redirect(url_for('main.home'))


@post.route('/compose/chirp', methods = ['GET', 'POST'])
@login_required
def compose_chirp():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(id = randbits(60), content = form.content.data, author = current_user)  # from the backref in db
        db.session.add(post)
        db.session.commit()
        flash('Your Chirp was sent. View')
        return redirect(url_for('user.profile', handle = current_user.handle))
    return render_template('compose_chirp.html', form = form)