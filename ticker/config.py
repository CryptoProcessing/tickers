class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'ticker_job',
            'func': 'controllers.tasks:ticker_job',
            'trigger': {
                'type': 'interval',
                'seconds': 240
            }
        }

    ]

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


class Config(object):
    SECRET_KEY = 'e21fa0fa3e0d28505c5d1b795495b2ee08420c71d036a9e2dee04cd0818ba70e'

    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'


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


