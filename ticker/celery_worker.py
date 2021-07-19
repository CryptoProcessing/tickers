import os

from ticker import create_app, make_celery

env = os.environ.get("TICKER_ENV", "prod")
celery = make_celery(create_app("config.%sConfig" % env.capitalize(), register_blueprints=False))
