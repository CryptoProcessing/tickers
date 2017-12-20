from flask import Flask, Blueprint
from ticker.models import db
from ticker.extensions import rest_api, app_scheduler, celery
from controllers.tasks import save_ticker
# from .controllers.rest import auth, transaction_api, account


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)

    # with app.app_context():
    db.app = app
    db.init_app(app)

    # start scheduler
    app_scheduler.init_app(app)
    app_scheduler.start()

    # init celery
    celery.init_app(app)

    auth_blueprint = Blueprint('auth', __name__)
    #
    # # define the API resources
    # registration_view = auth.RegisterAPI.as_view('register_api')
    # login_view = auth.LoginAPI.as_view('login_api')
    # user_view = auth.UserAPI.as_view('user_api')
    # logout_view = auth.LogoutAPI.as_view('logout_api')
    #
    # # add Rules for API Endpoints
    # auth_blueprint.add_url_rule(
    #     '/auth/register',
    #     view_func=registration_view,
    #     methods=['POST']
    # )
    # auth_blueprint.add_url_rule(
    #     '/auth/login',
    #     view_func=login_view,
    #     methods=['POST']
    # )
    # auth_blueprint.add_url_rule(
    #     '/auth/status/<account_id>',
    #     view_func=user_view,
    #     methods=['GET']
    # )
    # auth_blueprint.add_url_rule(
    #     '/auth/status',
    #     view_func=user_view,
    #     methods=['GET']
    # )
    # auth_blueprint.add_url_rule(
    #     '/auth/logout',
    #     view_func=logout_view,
    #     methods=['POST']
    # )

    app.register_blueprint(auth_blueprint, url_prefix='/api')

    rest_api.init_app(app)

    return app


if __name__ == '__main__':
    app = app = create_app('project.config.ProdConfig')
    app.run()
