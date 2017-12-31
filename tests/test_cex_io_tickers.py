import unittest
from controllers import cex_io
from unittest.mock import patch
from tests.response_mock.response_mock_cex import cexio_response, cexio_expected_response
import datetime


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_cexio_requests_get(*args, **kwargs):
    if args[0] == 'https://cex.io/api/tickers/BTC/USD':
        return MockResponse(cexio_response, 200)

    return MockResponse(None, 404)


def mocked_cexio_requests_get_none_resp(*args, **kwargs):
    if args[0] == 'https://cex.io/api/tickers/BTC/USD':
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_cexio_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == 'https://cex.io/api/tickers/BTC/USD':
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestUtils(unittest.TestCase):
    def test_map_fund_ok(self):
        clsinst = cex_io.Cexio()
        mapped_fund = clsinst.map_fund('BTC:USD')
        mapped_fund2 = clsinst.map_fund('ETH:BTC')

        self.assertEqual(mapped_fund, 'BTC:USD')
        self.assertEqual(mapped_fund2, 'ETH:BTC')

    def test_map_fund_not_found(self):
        clsinst = cex_io.Cexio()
        mapped_fund = clsinst.map_fund('BTG:UHD')

        self.assertEqual(mapped_fund, None)

    def test_str_to_date_ok(self):
        clsinst = cex_io.Cexio()
        mapped_fund = clsinst.map_fund('BTC:USD')
        mapped_fund2 = clsinst.map_fund('ETH:BTC')

        self.assertEqual(mapped_fund, 'BTC:USD')
        self.assertEqual(mapped_fund2, 'ETH:BTC')

    def test_str_todate(self):
        clsinst = cex_io.Cexio()
        mapped_fund = clsinst.str_to_date('1514561378')

        self.assertTrue(isinstance(mapped_fund, datetime.date))
        self.assertTrue(mapped_fund, datetime.datetime(2017, 12, 29, 18, 29, 38))


class Testcexio(unittest.TestCase):

    @patch('controllers.cex_io.requests.get', side_effect=mocked_cexio_requests_get)
    def test_cexio(self, _):

        cexio_trading = cex_io.Cexio(fund_ids=(
            ('BTC:USD', 'BTC:USD'),
            ('ETH:BTC', 'ETH:BTC'),
        ))
        response = cexio_trading.get_ticker_info()

        self.assertEqual(response, cexio_expected_response)

    @patch('controllers.cex_io.requests.get', side_effect=mocked_cexio_requests_get_none_resp)
    def test_cexio_none(self, _):

        cexio_trading = cex_io.Cexio()
        response = cexio_trading.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.cex_io.requests.get', side_effect=mocked_cexio_requests_get_empty__dict_resp)
    def test_cexio_empty_dict(self, _):

        cexio_trading = cex_io.Cexio()
        response = cexio_trading.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)