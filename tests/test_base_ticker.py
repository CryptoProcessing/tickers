import unittest
from controllers.markets import bitfinex
from tests.base import BaseTestCase


class TestBaseTicker(BaseTestCase):

    def setUp(self):

        self.bitfinex_resp = bitfinex.Bitfinex(fund_ids=(
            ('btcusd', 'BTC:USD', ),
            ('ethbtc', 'ETH:BTC', 1000),
        ))

    def test_factor_fail(self):

        f = self.bitfinex_resp.factor( ('btcusd', 'BTC:USD'))

        self.assertEqual(f, 1)

    def test_factor_success(self):

        f = self.bitfinex_resp.factor(('ethbtc', 'ETH:BTC', 1000))

        self.assertEqual(f, 1000)

    def test_factor_fail_txt(self):

        f = self.bitfinex_resp.factor(('ethbtc', 'ETH:BTC', 'fdfd'))

        self.assertEqual(f, 1)

    def test_default_request_timeout(self):
        timeout = self.bitfinex_resp.get_request_timeout()

        self.assertEqual(timeout, 5)

    def test_request_timeout(self):
        self.app.config['REQUEST_TIMEOUT'] = 100

        timeout = self.bitfinex_resp.get_request_timeout()

        self.assertEqual(timeout, 100)