import unittest
from controllers.markets import therocktrading
from unittest.mock import patch
from tests.response_mock.response_mock import therock_response, therock_expected_response
import datetime


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_therock_requests_get(*args, **kwargs):
    if args[0] == 'https://api.therocktrading.com/v1/funds/tickers':
        return MockResponse(therock_response, 200)

    return MockResponse(None, 404)


def mocked_therock_requests_get_none_resp(*args, **kwargs):
    if args[0] == 'https://api.therocktrading.com/v1/funds/tickers':
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_therock_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == 'https://api.therocktrading.com/v1/funds/tickers':
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestUtils(unittest.TestCase):
    def test_map_fund_ok(self):
        clsinst = therocktrading.Therocktrading()
        mapped_fund = clsinst.map_fund('BTCUSD')
        mapped_fund2 = clsinst.map_fund('ETHBTC')

        self.assertEqual(mapped_fund, 'BTC:USD')
        self.assertEqual(mapped_fund2, 'ETH:BTC')

    def test_map_fund_not_found(self):
        clsinst = therocktrading.Therocktrading()
        mapped_fund = clsinst.map_fund('BTGUHD')

        self.assertEqual(mapped_fund, None)

    def test_str_to_date_ok(self):
        clsinst = therocktrading.Therocktrading()
        mapped_fund = clsinst.map_fund('BTCUSD')
        mapped_fund2 = clsinst.map_fund('ETHBTC')

        self.assertEqual(mapped_fund, 'BTC:USD')
        self.assertEqual(mapped_fund2, 'ETH:BTC')

    def test_str_todate(self):
        clsinst = therocktrading.Therocktrading()
        mapped_fund = clsinst.str_to_date('2017-12-18T16:25:34.205+01:00')

        self.assertTrue(isinstance(mapped_fund, datetime.date))


class TestTherocktrading(unittest.TestCase):

    @patch('controllers.markets.therocktrading.requests.get', side_effect=mocked_therock_requests_get)
    def test_therocktrading(self, _):

        therock_trading = therocktrading.Therocktrading(fund_ids=(
            ('BTCUSD', 'BTC:USD'),
            ('ETHBTC', 'ETH:BTC'),
        ))
        response = therock_trading.get_ticker_info()

        self.assertEqual(response, therock_expected_response)

    @patch('controllers.markets.therocktrading.requests.get', side_effect=mocked_therock_requests_get_none_resp)
    def test_therocktrading_none(self, _):

        therock_trading = therocktrading.Therocktrading()
        response = therock_trading.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.markets.therocktrading.requests.get', side_effect=mocked_therock_requests_get_empty__dict_resp)
    def test_therocktrading_empty_dict(self, _):

        therock_trading = therocktrading.Therocktrading()
        response = therock_trading.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)