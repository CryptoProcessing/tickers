from flask import Flask, Blueprint
from ticker.models import db
from ticker.extensions import rest_api, app_scheduler, celery
from controllers.tasks import save_ticker
from controllers.api_controller import PriceApi


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)

    # with app.app_context():
    db.app = app
    db.init_app(app)

    # start scheduler
    app_scheduler.init_app(app)
    app_scheduler.start()

    # # init celery
    # celery.app = app
    # celery.init_app(app)

    auth_blueprint = Blueprint('auth', __name__)

    # define the API resources
    pricelast_view = PriceApi.as_view('last_price')

    # add Rules for API Endpoints
    auth_blueprint.add_url_rule(
        '/data/pricelast',
        view_func=pricelast_view,
        methods=['GET']
    )

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    rest_api.init_app(app)

    return app


if __name__ == '__main__':
    app = app = create_app('project.config.ProdConfig')
    app.run()
