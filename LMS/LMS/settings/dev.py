from .base import *

SECRET_KEY = 'django-insecure-d+qzxt3@tv+(87w53^j!ml3607^ba()cygs7f^6@fu^ov(=yx+'

DEBUG = True

ALLOWED_HOSTS =  ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'the_temple_of_knowledge',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = BASE_DIR, 'static'