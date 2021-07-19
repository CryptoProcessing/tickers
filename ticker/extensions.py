from flask_apscheduler import APScheduler
from flask_caching import Cache
from flask_restful import Api
from raven.contrib.flask import Sentry

rest_api = Api()
app_scheduler = APScheduler()
sentry = Sentry()
cache = Cache()
