from .base import *
import os


DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':get_secret_key('DB_NAME'),
        'USER':get_secret_key('DB_USER'),
        'PASSWORD':get_secret_key('DB_PWD'),
        'HOST':'localhost',
        'PORT':'5432',
    }
}


STATIC_URL = 'static/'
STATICFILES_DIRS = [
        os.path.join (BASE_DIR, "static"),
]

STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')

#para que se guarden las imagenes o media de los modelos
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join (BASE_DIR, "media") 