import unittest
from controllers import bitfinex
from unittest.mock import patch
from tests.response_mock.response_mock import bitfinex_response_btc_usd, bitfinex_response_eth_btc, bitfinex_expected_response
import datetime


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_bitfinex_requests_get(*args, **kwargs):
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/btcusd':
        return MockResponse(bitfinex_response_btc_usd, 200)
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/ethbtc':
        return MockResponse(bitfinex_response_eth_btc, 200)

    return MockResponse(None, 404)


def mocked_bitfinex_requests_get_none_resp(*args, **kwargs):
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/btcusd':
        return MockResponse(None, 404)
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/ethbtc':
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_bitfinex_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/btcusd':
        return MockResponse({}, 200)
    if args[0] == 'https://api.bitfinex.com/v1/pubticker/ethbtc':
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class Testbitfinex(unittest.TestCase):
    def setUp(self):
        self.bitfinex_resp = bitfinex.Bitfinex(fund_ids=(
            ('btcusd', 'BTC:USD'),
            ('ethbtc', 'ETH:BTC'),
        ))

    @patch('controllers.bitfinex.requests.get', side_effect=mocked_bitfinex_requests_get)
    def test_bitfinex(self, _):

        response = self.bitfinex_resp.get_ticker_info()

        self.assertEqual(response, bitfinex_expected_response)

    @patch('controllers.bitfinex.requests.get', side_effect=mocked_bitfinex_requests_get_none_resp)
    def test_bitfinex_resp_none(self, _):
        response = self.bitfinex_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.bitfinex.requests.get', side_effect=mocked_bitfinex_requests_get_empty__dict_resp)
    def test_bitfinex_empty_dict(self, _):
        response = self.bitfinex_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)