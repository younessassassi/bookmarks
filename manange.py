from thermos import app, db
from thermos.models import User
from flask.ext.script import Manager, Server, prompt_bool


manager = Manager(app)
manager.add_command("runserver", Server(port=5000, host='0.0.0.0'))

@manager.command
def initdb():
	db.create_all()
	db.session.add(User(username="youness", email="youness@example.com"))
	db.session.add(User(username="assassi", email="assassi@example.com"))
	db.session.commit()
	print 'Initialized the database'

@manager.command 
def dropdb():
	if prompt_bool("Please confirm dropping the database which will result in deleting all of its data"):
		db.drop_all()
		print 'Dropped the database'

if __name__ == '__main__':
	manager.run()