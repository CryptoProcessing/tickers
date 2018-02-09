import unittest
import datetime
import time
import json
from ticker.models import db
from ticker.models import Ticker, Pair, Market
from tests.base import BaseTestCase
from controllers.api_controller import PriceApi


class TestApiController(BaseTestCase):

    def setUp(self):
        super(TestApiController, self).setUp()

        self.pair_name = 'BTC:USD'
        self.pair_name2 = 'ETH:USD'

        self.market_name = 'Best market in the world'
        self.market_name2 = '2nd best market in the world'

        self.datetimeformat = "%Y-%m-%d %H:%M:%S"
        self.datetime = datetime.datetime.now().strftime(self.datetimeformat)

        self.market = Market(
            name=self.market_name,

        )
        db.session.add(self.market)
        db.session.commit()

        # 2nd market
        self.market2 = Market(
            name=self.market_name2,

        )
        db.session.add(self.market2)
        db.session.commit()

        # 1st pair
        self.pair = Pair(
            name=self.pair_name,

        )
        db.session.add(self.pair)
        db.session.commit()

        # 2nd pair
        self.pair2 = Pair(
            name=self.pair_name2,

        )
        db.session.add(self.pair2)
        db.session.commit()

        self.ticker = Ticker(
            date=self.datetime,
            pair=self.pair,
            bid=125.00,
            ask=125,
            market=self.market

        )
        db.session.add(self.ticker)
        db.session.commit()

        self.ticker2 = Ticker(
            date=self.datetime,
            pair=self.pair,
            bid=500.00,
            ask=500,
            market=self.market2

        )
        db.session.add(self.ticker2)
        db.session.commit()

        self.ticker3 = Ticker(
            date=self.datetime,
            pair=self.pair2,
            bid=100.00,
            ask=100,
            market=self.market

        )
        db.session.add(self.ticker3)
        db.session.commit()

        self.ticker4 = Ticker(
            date=self.datetime,
            pair=self.pair2,
            bid=150.00,
            ask=150,
            market=self.market2

        )
        db.session.add(self.ticker4)
        db.session.commit()

        time.sleep(1)
        self.midle_time = int(datetime.datetime.now().timestamp())
        time.sleep(1)

        self.ticker5 = Ticker(
            date=self.datetime,
            pair=self.pair2,
            bid=100.00,
            ask=100,
            market=self.market

        )
        db.session.add(self.ticker5)
        db.session.commit()

        self.ticker6 = Ticker(
            date=self.datetime,
            pair=self.pair2,
            bid=200.00,
            ask=200,
            market=self.market2

        )
        db.session.add(self.ticker6)
        db.session.commit()

        self.ticker7 = Ticker(
            date=self.datetime,
            pair=self.pair,
            bid=200.00,
            ask=200,
            market=self.market

        )
        db.session.add(self.ticker7)
        db.session.commit()

        self.ticker8 = Ticker(
            date=self.datetime,
            pair=self.pair,
            bid=600.00,
            ask=600,
            market=self.market2

        )
        db.session.add(self.ticker8)
        db.session.commit()

    def test_get_without_params_ok(self):
        api = PriceApi()
        result = api.query()
        self.assertEqual(result, [('BTC:USD', 400.00), ('ETH:USD', 150.0)])

    def test_get_timestamp_params_ok(self):
        api = PriceApi()
        result = api.query(ts=self.midle_time)
        self.assertEqual(result, [('BTC:USD', 312.50), ('ETH:USD', 125.0)])

    def test_get_pair_params_ok(self):
        api = PriceApi()
        result = api.query(pair='BTC:USD')
        self.assertEqual(result, [('BTC:USD', 400.0)])

    def test_get_pair_timestamp_params_ok(self):
        api = PriceApi()
        result = api.query(pair='BTC:USD', ts=self.midle_time)
        self.assertEqual(result, [('BTC:USD', 312.50)])

    def test_get_pair_params_not_ok(self):
        api = PriceApi()
        result = api.query(pair='BBB:UUU')
        self.assertEqual(result, [])

    def test_get_pair_market_params_ok(self):
        api = PriceApi()
        result = api.query(pair='BTC:USD', market=2)
        result2 = api.query(pair='ETH:USD', market=2)
        self.assertEqual(result, [('BTC:USD', 600.0)])
        self.assertEqual(result2, [('ETH:USD', 200.0)])

    def test_get_markets_list(self):

        response = self.client.get(
            '/api/v1/data/markets'
        )

        data = json.loads(response.data.decode())
        self.assertEqual(data, [{'name': 'Best market in the world', 'id': 1}, {'name': '2nd best market in the world', 'id': 2}])