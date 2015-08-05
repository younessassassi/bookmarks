from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user


from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, SignupForm


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully as {}.'.format(user.username))
            return redirect(request.args.get('next') or url_for('bookmarks.user', username=user.username))
        flash('incorrect username or password.')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please Login.'.format(user.username))
        return redirect(url_for('.login'))
    return render_template("signup.html", form=form)
