import os

from .settings import *

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "service": "automata",
            "passfile": ".pgpass",
        },
    }
}


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["application/x-python-serialize"]
