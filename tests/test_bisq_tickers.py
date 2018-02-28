import unittest
from controllers import bisq_network
from unittest.mock import patch, Mock
from tests.response_mock.response_bisq_network import response_btc_usd, response_eth_btc
import datetime

ETH_BTC_URL = 'https://markets.bisq.network/api/ticker?market=eth_btc'
BTC_USD_URL = 'https://markets.bisq.network/api/ticker?market=btc_usd'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestUtils(unittest.TestCase):

    def test_str_todate(self):
        clsinst = bisq_network.Bisq()
        mapped_fund = clsinst.str_to_date(None)

        self.assertTrue(isinstance(mapped_fund, datetime.date))


def mocked_requests_get(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(response_btc_usd, 200)
    if args[0] == ETH_BTC_URL:
        return MockResponse(response_eth_btc, 200)

    return MockResponse(None, 404)


def mocked_requests_get_none_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(None, 404)
    if args[0] == ETH_BTC_URL:
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse({}, 200)
    if args[0] == ETH_BTC_URL:
        return MockResponse({}, 200)

    return MockResponse(None, 404)


dtm = datetime.datetime.now()


class TestBisq(unittest.TestCase):
    def setUp(self):
        self.bitsmap_net_resp = bisq_network.Bisq(fund_ids=(
            ('btc_usd', 'BTC:USD'),
            ('eth_btc', 'ETH:BTC'),
        ))

    @patch('controllers.base_ticker.datetime', Mock(now=lambda: dtm))
    @patch('controllers.bisq_network.requests.get', side_effect=mocked_requests_get)
    def test_bitsmap_net(self, _):
        expected_response = [
            {'ask': 9468.36000000,
             'bid': 9468.36000000,
             'date': dtm,
             'fund_id': 'BTC:USD'},
            {'ask': 0.10184646,
             'bid': 0.10184646,
             'date': dtm,
             'fund_id': 'ETH:BTC'}
        ]

        response = self.bitsmap_net_resp.get_ticker_info()

        self.assertEqual(response, expected_response)

    @patch('controllers.bisq_network.requests.get', side_effect=mocked_requests_get_none_resp)
    def test_bitsmap_net_resp_none(self, _):
        response = self.bitsmap_net_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.bisq_network.requests.get', side_effect=mocked_requests_get_empty__dict_resp)
    def test_bitsmap_net_empty_dict(self, _):
        response = self.bitsmap_net_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)