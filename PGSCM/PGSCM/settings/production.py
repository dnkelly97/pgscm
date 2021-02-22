from PGSCM.settings.common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresProduction',
        'USER': 'postgres',
        'PASSWORD': 'temppassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = 'hjhj'

ALLOWED_HOSTS = []

# TODO: The settings for production environment need to be configured. This includes but is not limited to
#  setting the secret key and allowed hosts. For more informtion about deployment configurations see
#  https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/