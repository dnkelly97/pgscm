from PGSCM.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j04#7k2y*#1y%)54it3h1ve^2#iafyq-%^d$6sw1ceg58j-m!h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'temppassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']
