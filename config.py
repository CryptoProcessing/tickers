import os
import raven


class SchedulerConfig:
    JOBS = [
        {
            'id': 'ticker_job',
            'func': 'controllers.tasks:ticker_job',
            'trigger': {
                'type': 'interval',
                'seconds': 300
            }
        }
    ]

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 25}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 25
    }

    SCHEDULER_API_ENABLED = True


class Config:
    SECRET_KEY = 'e21fa0fa3e0d28505c5d1b795495b2ee08420c71d036a9e2dee04cd0818ba70e'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    OPENEXCHANGERATES_API_KEY = '081be513ea2d4d1ea394bf528ecb137f'

    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 3600  # one hour
    CACHE_KEY_PREFIX = '_cache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'


class ProdConfig(Config, SchedulerConfig):
    DEBUG = False
    APP_SCHEDULER_START = True
    MYSQL = {
        'user': 'tickers',
        'pw': 'tickers',
        'db': 'tickers',
        'host': 'localhost',
        'port': '3306',
    }
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % MYSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENTRY_CONFIG = {
        'dsn': 'https://6eed6a3f6aab4317b6337a43f589287f:4ed9a516518f42b2ae7434988853d15d@sentry.io/265553',
        'include_paths': ['Tickers'],
        'release': raven.fetch_git_sha(os.path.dirname(__file__)),
    }
    REQUEST_TIMEOUT = 5

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


class DevConfig(Config, SchedulerConfig):
    DEBUG = False
    APP_SCHEDULER_START = True
    MYSQL = {
        'user': 'tickers',
        'pw': 'tickers',
        'db': 'tickers',
        'host': 'localhost',
        'port': '3306',
    }
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % MYSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEBUG = True
    APP_SCHEDULER_START = False
    MYSQL = {
        'user': 'tickers',
        'pw': 'tickers',
        'db': 'tickers_test',
        'host': 'localhost',
        'port': '3306',
    }
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % MYSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


