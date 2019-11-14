from flask_restful import Api
from flask_apscheduler import APScheduler
from flask_celery import Celery
from raven.contrib.flask import Sentry
from flask_caching import Cache


rest_api = Api()
app_scheduler = APScheduler()
sentry = Sentry()
cache = Cache()
