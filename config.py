import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

# load environment variables from a file named .env in the current directory or any of its parents or from the path specificied
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'myLibrary.db')
    SQLALCHEMY_TRACK_MODIFICATIONS =False