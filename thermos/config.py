import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = '/B]\x06L.\xab\xa4^\x93:}\xc2\x13\xbea\xaa\xcc\x1c\x1f5vq\xad'
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
	    os.path.join(basedir, 'thermos.db')

class TestingConfig(Config):
	Testing = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
	    os.path.join(basedir, 'data-test.db')
	WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
	    os.path.join(basedir, 'thermos.db')

config_by_name = dict(
	dev = DevelopmentConfig,
	test = TestingConfig,
	prod = ProductionConfig
)