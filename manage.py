from thermos import app, db
from thermos.models import User, Bookmark
from flask.ext.script import Manager, Server, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server(port=5000, host='0.0.0.0'))
manager.add_command('db', MigrateCommand)

@manager.command
def insert_users():
	db.session.add(User(username="youness", email="youness@example.com", password="test"))
	db.session.add(User(username="assassi", email="assassi@example.com", password="test"))
	db.session.commit()
	print 'users added'

# @manager.command
# def initdb():
#     db.create_all()
#     db.session.add(User(username="youness", email="youness@example.com", password="test"))
#     db.session.add(User(username="assassi", email="assassi@example.com", password="test"))
#     db.session.commit()
#     print 'Initialized the database'


@manager.command
def dropdb():
    if prompt_bool("Please confirm dropping the database which will result in deleting all of its data"):
        db.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()
