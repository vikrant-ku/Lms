from .base import *

SECRET_KEY = 'django-insecure-d+qzxt3@tv+(87w53^j!ml3607^ba()cygs7f^6@fu^ov(=yx+'

DEBUG = True

ALLOWED_HOSTS = ["128.199.28.181"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')