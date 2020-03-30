import unittest
from tests.base import BaseTestCase

from controllers.markets import bitstamp
from unittest.mock import patch
from tests.response_mock.response_bitstamp_network import response_btc_usd, response_eth_btc, expected_response

btc_usd_url = 'https://www.bitstamp.net/api/v2/ticker/btcusd/'
eth_btc_url = 'https://www.bitstamp.net/api/v2/ticker/ethbtc/'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_bitstamp_requests_get(*args, **kwargs):
    if args[0] == btc_usd_url:
        return MockResponse(response_btc_usd, 200)
    if args[0] == 'https://www.bitstamp.net/api/v2/ticker/ethbtc/':
        return MockResponse(response_eth_btc, 200)

    return MockResponse(None, 404)


def mocked_bitstamp_requests_get_none_resp(*args, **kwargs):
    if args[0] == btc_usd_url:
        return MockResponse(None, 404)
    if args[0] == eth_btc_url:
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_bitstamp_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == btc_usd_url:
        return MockResponse({}, 200)
    if args[0] == eth_btc_url:
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestBitstamp(BaseTestCase):
    def setUp(self):

        self.bitstamp_resp = bitstamp.Bitstamp(fund_ids=(
            ('btcusd', 'BTC:USD'),
            ('ethbtc', 'ETH:BTC'),
        ))

    @patch('controllers.base_ticker.requests.get', side_effect=mocked_bitstamp_requests_get)
    def test_bitstamp(self, _):
        response = self.bitstamp_resp.get_ticker_info()

        self.assertEqual(response, expected_response)

    @patch('controllers.base_ticker.requests.get', side_effect=mocked_bitstamp_requests_get_none_resp)
    def test_bitstamp_resp_none(self, _):
        response = self.bitstamp_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.base_ticker.requests.get', side_effect=mocked_bitstamp_requests_get_empty__dict_resp)
    def test_bitstamp_empty_dict(self, _):
        response = self.bitstamp_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)