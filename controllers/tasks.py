import datetime
from flask import current_app
from controllers.therocktrading import Therocktrading
from controllers.gdax import Gdax
from ticker.extensions import celery
from ticker.models import Ticker, get_one_or_create, Market, Pair, db


#  add all tickers classes

MAP_PROVIDER = {
    'therocktrading.com': Therocktrading(),
    'GDAX': Gdax(),
}


# @celery.task()
def save_ticker(mp):
    provider = InfoProvider(resource=mp)
    ticker_data = provider.get_tickers()
    # current_app.logger.debug('New record in db {}'.format(mp))
    # with app.app_context():
    to_db(market=mp, data=ticker_data)


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


def ticker_job():
    for mp in MAP_PROVIDER:
        print(datetime.datetime.now())
        save_ticker(mp)


class InfoProvider:

    def __init__(self, resource):
        self.resource = resource

    def _connect_to(self, resource):
        factory = None
        try:
            factory = MAP_PROVIDER.get(resource)
        except KeyError as e:
            print(e)
        return factory

    def get_tickers(self):
        factory = self._connect_to(self.resource)
        try:
            response = factory.get_ticker_info()
            return response

        except Exception as e:
            current_app.logger.warning('Error tickers info server {} {}'.format(self.resource, e))

