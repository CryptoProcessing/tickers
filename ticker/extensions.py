from flask_restful import Api
from flask_apscheduler import APScheduler
from flask_celery import Celery


celery = Celery()
rest_api = Api()
app_scheduler = APScheduler()
