import unittest
from tests.base import BaseTestCase

from controllers.markets import gdax
from unittest.mock import patch
from tests.response_mock.response_mock import gdax_response_btc_usd, gdax_response_eth_btc, gdax_expected_response


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_gdax_requests_get(*args, **kwargs):
    if args[0] == 'https://api.gdax.com/products/BTC-USD/ticker':
        return MockResponse(gdax_response_btc_usd, 200)
    if args[0] == 'https://api.gdax.com/products/ETH-BTC/ticker':
        return MockResponse(gdax_response_eth_btc, 200)

    return MockResponse(None, 404)


def mocked_gdax_requests_get_none_resp(*args, **kwargs):
    if args[0] == 'https://api.gdax.com/products/BTC-USD/ticker':
        return MockResponse(None, 404)
    if args[0] == 'https://api.gdax.com/products/ETH-BTC/ticker':
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_gdax_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == 'https://api.gdax.com/products/BTC-USD/ticker':
        return MockResponse({}, 200)
    if args[0] == 'https://api.gdax.com/products/ETH-BTC/ticker':
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestGdax(BaseTestCase):
    def setUp(self):

        self.gdax_resp = gdax.Gdax(fund_ids=(
            ('BTC-USD', 'BTC:USD'),
            ('ETH-BTC', 'ETH:BTC'),
        ))

    @patch('controllers.markets.gdax.requests.get', side_effect=mocked_gdax_requests_get)
    def test_gdax(self, _):
        response = self.gdax_resp.get_ticker_info()

        self.assertEqual(response, gdax_expected_response)

    @patch('controllers.markets.gdax.requests.get', side_effect=mocked_gdax_requests_get_none_resp)
    def test_gdax_resp_none(self, _):
        response = self.gdax_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.markets.gdax.requests.get', side_effect=mocked_gdax_requests_get_empty__dict_resp)
    def test_gdax_empty_dict(self, _):
        response = self.gdax_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)