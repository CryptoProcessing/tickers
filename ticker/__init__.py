from flask import Flask, Blueprint
from ticker.models import db
from ticker.extensions import rest_api, app_scheduler, sentry, cache
from controllers.api_controller import PriceApi, MarketApi, VersionApi

from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    # To have an access to app
    celery.app = app

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def create_app(object_name, register_blueprints=True):

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.app = app
    db.init_app(app)

    sentry.init_app(app)
    cache.init_app(app)

    if register_blueprints:

        auth_blueprint = Blueprint('auth', __name__)

        # define the API resources
        price_view = PriceApi.as_view('price')
        market_view = MarketApi.as_view('markets')
        version_view = VersionApi.as_view('version')
        # add Rules for API Endpoints
        auth_blueprint.add_url_rule(
            '/v1/data/price',
            view_func=price_view,
            methods=['GET']
        )
        auth_blueprint.add_url_rule(
            '/v1/data/markets',
            view_func=market_view,
            methods=['GET']
        )

        auth_blueprint.add_url_rule(
            '/version',
            view_func=version_view,
            methods=['GET']
        )
        app.register_blueprint(auth_blueprint, url_prefix='/api')

    rest_api.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app('project.config.ProdConfig')
    app.run()
