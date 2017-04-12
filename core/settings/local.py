import os

from .base import *


SECRET_KEY = os.environ['SECRET_KEY']
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']

DEBUG = True
ALLOWED_HOSTS = []
