# flake8: noqa
from .celery import app as celery_app
from .json_encodor import JSONEncoder

# これがあるとwsgiが動かない気がする
__all__ = ("celery_app",)
