import datetime
import unittest
from unittest.mock import patch

from controllers.markets import itbit_com
from tests.base import BaseTestCase
from tests.response_mock.response_itbit_com import (itbit_expected_response,
                                                    itbit_response_btc_usd)

BTC_USD_URL = 'https://api.itbit.com/v1/markets/XBTUSD/ticker'


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(itbit_response_btc_usd, 200)

    return MockResponse(None, 404)


def mocked_requests_get_none_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse(None, 404)

    return MockResponse(None, 404)


def mocked_requests_get_empty__dict_resp(*args, **kwargs):
    if args[0] == BTC_USD_URL:
        return MockResponse({}, 200)

    return MockResponse(None, 404)


class TestUtils(BaseTestCase):
    def setUp(self):
        super(TestUtils, self).setUp()
        self.clsinst = itbit_com.Itbit()
            
    def test_map_fund_ok(self):
        
        mapped_fund = self.clsinst.map_fund('XBTUSD')

        self.assertEqual(mapped_fund, 'BTC:USD')

    def test_map_fund_not_found(self):
        mapped_fund = self.clsinst.map_fund('BTGUHD')

        self.assertEqual(mapped_fund, None)

    def test_str_todate(self):
        mapped_fund = self.clsinst.str_to_date('2018-02-14T20:34:24.4785988Z')

        self.assertTrue(isinstance(mapped_fund, datetime.date))
        self.assertEqual(mapped_fund, datetime.datetime(2018, 2, 14, 20, 34, 24))


class TestiIbit(BaseTestCase):
    def setUp(self):
        super(TestiIbit, self).setUp()
        self.itbit_com_resp = itbit_com.Itbit()
        
    @patch('controllers.base_ticker.requests.get', side_effect=mocked_requests_get)
    def test_itbit_com(self, _):
        itbit_com_resp = itbit_com.Itbit(fund_ids=(
            ('XBTUSD', 'BTC:USD'),
        ))
        response = itbit_com_resp.get_ticker_info()

        self.assertEqual(response, itbit_expected_response)

    @patch('controllers.base_ticker.requests.get', side_effect=mocked_requests_get_none_resp)
    def test_itbit_com_resp_none(self, _):
        response = self.itbit_com_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)

    @patch('controllers.base_ticker.requests.get', side_effect=mocked_requests_get_empty__dict_resp)
    def test_itbit_com_empty_dict(self, _):
        response = self.itbit_com_resp.get_ticker_info()
        expected_response = []

        self.assertEqual(response, expected_response)