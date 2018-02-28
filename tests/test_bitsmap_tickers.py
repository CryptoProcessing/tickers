import unittest
from controllers import bitsmap_net
from unittest.mock import patch
from tests.response_mock.response_www_bitstamp_net import bitsmap_expected_response, bitsmap_response_btc_usd, bitsmap_response_eth_usd
import datetime

ETH_USD_URL = 'https://www.bitstamp.net/api/v2/ticker/ethusd'
BTC_USD_URL = 'https://www.bitstamp.net/api/v2/ticker/btcusd'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(bitsmap_response_btc_usd, 200)
    if args[0] == ETH_USD_URL:
        return MockResponse(bitsmap_response_eth_usd, 200)

    return MockResponse(None, 404)


def mocked_requests_get_none_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(None, 404)
    if args[0] == ETH_USD_URL:
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse({}, 200)
    if args[0] == ETH_USD_URL:
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestGdax(unittest.TestCase):
    def setUp(self):
        self.bitsmap_net_resp = bitsmap_net.Bitsmap(fund_ids=(
            ('btcusd', 'BTC:USD'),
            ('ethusd', 'ETH:USD'),
        ))

    @patch('controllers.bitsmap_net.requests.get', side_effect=mocked_requests_get)
    def test_bitsmap_net(self, _):

        response = self.bitsmap_net_resp.get_ticker_info()

        self.assertEqual(response, bitsmap_expected_response)

    @patch('controllers.bitsmap_net.requests.get', side_effect=mocked_requests_get_none_resp)
    def test_bitsmap_net_resp_none(self, _):
        response = self.bitsmap_net_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.bitsmap_net.requests.get', side_effect=mocked_requests_get_empty__dict_resp)
    def test_bitsmap_net_empty_dict(self, _):
        response = self.bitsmap_net_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)