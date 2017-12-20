import unittest
import datetime
from ticker.models import db
from ticker.models import Ticker, Pair, Market
from tests.base import BaseTestCase


class TestModel(BaseTestCase):

    def setUp(self):
        super(TestModel, self).setUp()

        self.pair_name = 'BTC_USD'
        self.market_name = 'Best market in the world'
        self.datetimeformat = "%Y-%m-%d %H:%M:%S"
        self.datetime = datetime.datetime.now().strftime(self.datetimeformat)

        self.market = Market(
            name=self.market_name,

        )
        db.session.add(self.market)
        db.session.commit()

        self.pair = Pair(
            name=self.pair_name,

        )
        db.session.add(self.pair)
        db.session.commit()

        self.ticker = Ticker(
            date=self.datetime,
            pair=self.pair,
            bid=125.00,
            ask=0.12365454545,
            market=self.market

        )
        db.session.add(self.ticker)
        db.session.commit()

    def test_pair_market_ok(self):

        self.assertEqual(self.pair.name, self.pair_name)
        self.assertTrue(self.pair.id)

    def test_market_ok(self):

        self.assertEqual(self.market.name, self.market_name)
        self.assertTrue(self.market.id)

    def test_ticker_ok(self):
        self.assertTrue(self.ticker.id)
        self.assertEqual(self.ticker.date, datetime.datetime.strptime(self.datetime, self.datetimeformat))
        self.assertEqual(self.ticker.pair, self.pair)
        self.assertEqual(self.ticker.bid, 125.00)
        self.assertEqual(self.ticker.ask, 0.12365454545)
        self.assertEqual(self.ticker.market, self.market)


if __name__ == '__main__':
    unittest.main()