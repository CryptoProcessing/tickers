import unittest
import json
import requests
from unittest.mock import patch, Mock, MagicMock
from controllers.markets import bitfinex
from tests.base import BaseTestCase
from tenacity import wait_none


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


def mock_request_get(*args, **kwargs):

    mock_response = kwargs
    return MockResponse(mock_response)


class TestBaseTicker(BaseTestCase):

    def setUp(self):

        self.bitfinex_resp = bitfinex.Bitfinex(fund_ids=(
            ('btcusd', 'BTC:USD', ),
            ('ethbtc', 'ETH:BTC', 1000),
        ))

    def test_factor_fail(self):

        f = self.bitfinex_resp.factor(('btcusd', 'BTC:USD'))

        self.assertEqual(f, 1)

    def test_factor_success(self):

        f = self.bitfinex_resp.factor(('ethbtc', 'ETH:BTC', 1000))

        self.assertEqual(f, 1000)

    def test_factor_fail_txt(self):

        f = self.bitfinex_resp.factor(('ethbtc', 'ETH:BTC', 'fdfd'))

        self.assertEqual(f, 1)

    def test_default_request_timeout(self):
        timeout = self.bitfinex_resp._get_request_timeout()

        self.assertEqual(timeout, 5)

    def test_request_timeout(self):
        self.app.config['REQUEST_TIMEOUT'] = 100

        timeout = self.bitfinex_resp._get_request_timeout()

        self.assertEqual(timeout, 100)

    @patch('controllers.base_ticker.requests.get')
    def test_request(self, mock_req):
        res = {'key': 'value'}

        mock_req.return_value = MockResponse(res)

        req = self.bitfinex_resp.make_request(url='url')

        self.assertEqual(req, res)

        self.assertEqual(mock_req.call_count, 1)

    @patch('controllers.base_ticker.requests.get')
    def test_request_fail(self, mock_req):
        mock_req.side_effect = requests.ConnectTimeout(*["Exception message"])

        # disable waiting for test
        self.bitfinex_resp.make_request.retry.wait = wait_none()

        with self.assertRaises(Exception) as e:
            req = self.bitfinex_resp.make_request(url='url')

        self.assertEqual(mock_req.call_count, 5)