from .common import *

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "drf-practice",
        "USER": "root",
        "PASSWORD": "0000",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1", "localhost"]
