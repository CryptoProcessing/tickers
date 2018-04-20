#!/usr/bin/env python

import os
import unittest
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from ticker import create_app
from ticker.models import db

from controllers.tasks import ticker_job
from controllers.utils import get_version


# default to dev config
env = os.environ.get('TICKER_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,

    )


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def runtickers():
    """Runs the tickers job."""
    ticker_job()


@manager.command
def version():
    """Runs the tickers job."""
    v = get_version()
    print(v)


if __name__ == "__main__":

    manager.run()
