from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from blogapp.forms.auth import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from blogapp import bcrypt, db, login_manager
from blogapp.models import User, Post
from blogapp.utils.auth import save_picture, send_reset_email


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.landing"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("index.landing"))
        else:
            flash("Email and or password are incorrect. Please try again.", "danger")

    return render_template("auth/login.html", title = "Login", form = form)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index.landing"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered your account! You can now login!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title = "Register", form = form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out!", "success")
    return redirect(url_for("index.landing"))


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account was successfully updated!", "success")
        return redirect(url_for("auth.account"))

    form.username.data = current_user.username
    form.email.data = current_user.email

    posts = current_user.posts

    return render_template("auth/account.html", title = "Account", form = form, posts = posts)


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash("You can't reset your password if you are already logged in", "danger")
        return redirect(url_for("posts.explore"))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("auth.login"))

    return render_template('auth/reset_request.html', title = 'Reset Password', form = form)


@auth.route("/reset_password<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash("You can't reset your password if you are already logged in", "danger")
        return redirect(url_for("posts.explore"))
    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_token.html', title='Reset Password', form=form)
