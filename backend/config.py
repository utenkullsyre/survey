import os

# You need to replace the next values with the appropriate values for your configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///sitat.sqlite3'
SECRET_KEY = "flabbergast"
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
