from flask import render_template, url_for, request, redirect, flash
from thermos import app, db
from forms import BookmarkForm
from models import User, Bookmark


# fake login 
def logged_in_user():
	return User.query.filter_by(username='assassi').first()



@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['POST', 'GET'])
def add():
	form = BookmarkForm()
	if form.validate_on_submit():
		url = form.url.data
		description = form.description.data
		bm = Bookmark(url=url, description=description, user=logged_in_user())
		db.session.add(bm)
		db.session.commit()
		flash("stored bookmark '{}'".format(description))
		return redirect(url_for('index'))
	return render_template('add.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500