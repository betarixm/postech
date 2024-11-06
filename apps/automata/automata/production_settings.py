import os

from .settings import *

secret_key_file = os.getenv("DJANGO_SECRET_KEY_FILE")
assert secret_key_file is not None, "DJANGO_SECRET_KEY_FILE is not set"

SECRET_KEY = open(secret_key_file).read().strip()

DEBUG = False

database_password_file = os.getenv("DATABASE_PASSWORD_FILE")
assert database_password_file is not None, "DATABASE_PASSWORD_FILE is not set"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "automata",
        "USER": "automata",
        "PASSWORD": open(database_password_file).read().strip(),
        "HOST": "database",
        "PORT": "5432",
    }
}


CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["application/x-python-serialize"]

ALLOWED_HOSTS = ["*"]
