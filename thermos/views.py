from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Bookmark

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(url=url, description=description, user=current_user)
        db.session.add(bm)
        db.session.commit()
        flash("stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('bookmark_form.html', form=form, title="Add new URL")

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title="Edit bookmark")

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully as {}.'.format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('incorrect username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please Login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
