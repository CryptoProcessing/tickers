from flask import Flask, Blueprint
from ticker.models import db
from ticker.extensions import rest_api, app_scheduler, celery
from controllers.api_controller import PriceApi


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)

    db.app = app
    db.init_app(app)

    # start scheduler
    app_scheduler.init_app(app)
    app_scheduler.start()

    auth_blueprint = Blueprint('auth', __name__)

    # define the API resources
    price_view = PriceApi.as_view('price')

    # add Rules for API Endpoints
    auth_blueprint.add_url_rule(
        '/data/price',
        view_func=price_view,
        methods=['GET']
    )

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    rest_api.init_app(app)

    return app


if __name__ == '__main__':
    app = app = create_app('project.config.ProdConfig')
    app.run()
