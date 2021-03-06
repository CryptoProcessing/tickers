import os

from controllers.markets.binance import Binance
from controllers.markets.kraken import Kraken
from controllers.markets.cex_io import Cexio
from ticker.extensions import sentry
from ticker.models import Ticker, get_one_or_create, Market, Pair, db
from ticker import make_celery, create_app

#  add all tickers classes

MAP_PROVIDER = {
    'cex.io': Cexio(),
    'binance.com': Binance(),
    'kraken.com': Kraken(),
}

env = os.environ.get('TICKER_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize(), register_blueprints=False)

celery = make_celery(app)


def ticker_job():
    for mp in MAP_PROVIDER:
        save_ticker(mp)


@celery.task()
def save_ticker(mp):
    provider = InfoProvider(resource=mp)
    try:
        market_alias = provider.get_class_name()
        ticker_data = provider.get_tickers()
        to_db(market=mp, market_alias=market_alias, data=ticker_data)
    except Exception as e:
        sentry.captureException()


def to_db(market, market_alias, data):
    """

    :param market:
    :param market_alias: get from class name
    :param data:
    :return:
    """
    for d in data:
        with db.app.app_context():
            market_db, _ = get_one_or_create(db.session, Market, name=market, alias=market_alias)
            pair_db, _ = get_one_or_create(db.session, Pair, name=d['fund_id'])

            ticker = Ticker(
                date=d['date'],
                pair=pair_db,
                bid=d['bid'],
                ask=d['ask'],
                market=market_db
            )

            db.session.add(ticker)
            db.session.commit()


class InfoProvider:

    def __init__(self, resource):
        self.resource = resource

    def _connect_to(self, resource):
        factory = None
        try:
            factory = MAP_PROVIDER.get(resource)
        except KeyError as e:
            sentry.captureException()
        return factory

    def get_tickers(self):
        factory = self._connect_to(self.resource)
        response = factory.get_ticker_info()

        return response

    def get_class_name(self):
        factory = MAP_PROVIDER.get(self.resource)
        class_name = factory.__class__.__name__
        return class_name.lower()





