import datetime
import os
from controllers.therocktrading import Therocktrading
from controllers.gdax import Gdax
from controllers.bitfinex import Bitfinex
from controllers.cex_io import Cexio
from controllers.bitsmap_net import Bitsmap
from controllers.itbit_com import Itbit
from controllers.bisq_network import Bisq
from ticker.extensions import sentry
from ticker.models import Ticker, get_one_or_create, Market, Pair, db
from ticker import make_celery, create_app

#  add all tickers classes

MAP_PROVIDER = {
    'therocktrading.com': Therocktrading(),
    'GDAX': Gdax(),
    'bitfinex.com': Bitfinex(),
    'cex.io': Cexio(),
    'bitsmap.net': Bitsmap(),
    'itbit.com': Itbit(),
    'bisq.network': Bisq()
}

env = os.environ.get('TICKER_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize(), register_blueprints=False)

celery = make_celery(app)


def ticker_job():
    for mp in MAP_PROVIDER:
        print(mp)
        save_ticker(mp)


@celery.task()
def save_ticker(mp):
    provider = InfoProvider(resource=mp)
    try:
        ticker_data = provider.get_tickers()
        to_db(market=mp, data=ticker_data)
    except Exception as e:
        sentry.captureException()


def to_db(market, data):
    for d in data:
        with db.app.app_context():
            market_db, _ = get_one_or_create(db.session, Market, name=market)
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





