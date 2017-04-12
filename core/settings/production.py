import os

from .base import *


SECRET_KEY = os.getenv('SECRET_KEY')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

DEBUG = False
ALLOWED_HOSTS = []
