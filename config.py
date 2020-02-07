import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # For security, I guess?
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # For SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



