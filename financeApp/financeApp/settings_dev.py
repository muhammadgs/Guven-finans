"""Development settings overriding the production defaults."""

import os

os.environ.setdefault("DJANGO_SECRET_KEY", "dev-secret-key")
os.environ.setdefault("DJANGO_DEBUG", "True")

from .settings import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]
