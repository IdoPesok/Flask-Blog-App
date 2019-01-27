from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from blogapp.forms.posts import PostForm, UpdatePostForm
from blogapp import bcrypt, db
from blogapp.models import Post, User


posts = Blueprint('posts', __name__)


@posts.route("/posts/explore")
def explore():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template("posts/explore.html", title = "Explore", posts = posts)


@posts.route("/posts/users/<int:user_id>")
def users(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user.id)
    return render_template("posts/users.html", title = user.username, posts = posts, user = user)


@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, image_url = form.imageUrl.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now up for all to see!", "success")
        return redirect(url_for("posts.explore"))

    return render_template("posts/new.html", title = "Post", form = form)


@posts.route("/posts/<int:post_id>")
def show(post_id):
    post = Post.query.get_or_404(post_id)
    post.comments.reverse()
    return render_template('posts/show.html', title = post.title, post = post)


@posts.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(post_id):
    form = UpdatePostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You must own that post to edit it!", "danger")
        return redirect(url_for("posts.show", post_id = post_id))

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_url = form.imageUrl.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.show", post_id = post_id))

    form.title.data = post.title
    form.content.data = post.content
    form.imageUrl.data = post.image_url

    return render_template('posts/edit.html', title = post.title, post = post, form = form)


@posts.route("/posts/<int:post_id>/delete")
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You must own that post to delete it!", "danger")
        return redirect(url_for("posts.show", post_id = post_id))

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for("posts.explore"))

