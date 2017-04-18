import os

from .base import *


SECURE_SSL_HOSTS = True

SECRET_KEY = os.getenv('SECRET_KEY')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

DEBUG = False
ALLOWED_HOSTS = []

# security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
