from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'core',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smartdoc_db',
        'USER': 'postgres',
        'PASSWORD': '112233',  # Replace with your real password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
