import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '/B]\x06L.\xab\xa4^\x93:}\xc2\x13\xbea\xaa\xcc\x1c\x1f5vq\xad'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True


db = SQLAlchemy(app)

import models
import views