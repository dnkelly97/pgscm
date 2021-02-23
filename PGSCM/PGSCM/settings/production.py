from PGSCM.settings.common import *
import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresProduction',
        'USER': 'postgres',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = []

# TODO: The settings for production environment need to be configured. This includes but is not limited to
#  setting the secret key , DB password and allowed hosts. For more informtion about deployment configurations
#  see https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/