from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]
CELERY_TASK_ALWAYS_EAGER = env.bool("CELERY_TASK_ALWAYS_EAGER", default=False)  # noqa
