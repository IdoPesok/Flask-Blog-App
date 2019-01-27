from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from blogapp import login_manager
from blogapp.models import Post, Comment
from blogapp.forms.comments import CommentForm, UpdateCommentForm
from blogapp import db


comments = Blueprint('comments', __name__)


@comments.route("/posts/<int:post_id>/comments/new", methods=['GET', 'POST'])
@login_required
def new(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment is now up for all to see!", "success")
        return redirect(url_for('posts.show', post_id=post.id))


    post = Post.query.get_or_404(post_id)
    return render_template("comments/new.html", title = "New Comment", form = form, post = post)


@comments.route("/posts/<int:post_id>/comments/<int:comment_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(post_id, comment_id):
    form = UpdateCommentForm()
    comment = Comment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)

    if comment.author != current_user:
        flash("You must own the comment to edit it!", "danger")
        return redirect("posts.show", post_id=post_id)

    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash("Your comment has been updated!", "success")
        return redirect(url_for('posts.show', post_id=post.id))

    form.content.data = comment.content

    return render_template("comments/edit.html", title = "New Comment", form = form, post = post, comment = comment)


@comments.route("/posts/<int:post_id>/comments/<int:comment_id>/delete")
@login_required
def delete(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)

    if comment.author != current_user:
        flash("You must own the comment to edit it!", "danger")
        return redirect("posts.show", post_id=post_id)

    db.session.delete(comment)
    db.session.commit()

    flash("Your comment has been deleted", "success")
    return redirect(url_for("posts.show", post_id=post_id))

