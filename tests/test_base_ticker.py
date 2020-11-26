import requests
from unittest.mock import patch
from controllers.markets import bitfinex
from tests.base import BaseTestCase
from tenacity import wait_none
from controllers.exchange_rates import openexchangerates, ecb


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


class MockResponseExch:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockResponseEcb:
    def __init__(self, text, status_code):
        self.status_code = status_code
        self.text = text

    def text(self):
        return self.text


def mock_request_get(*args, **kwargs):

    mock_response = kwargs
    return MockResponse(mock_response)


def mocked_open_exchange_rates(*args, **kwargs):
    if 'https://openexchangerates.org/api/' in args[0]:
        return MockResponseExch({
            "disclaimer": "Usage subject to terms: https://openexchangerates.org/terms",
            "license": "https://openexchangerates.org/license",
            "timestamp": 1573725600,
            "base": "USD",
            "rates": {
                "AUD": 1.471887,
                "GBP": 0.778172,
                "RUB": 64.13375
            }
        }, 200)

    return MockResponseExch(None, 404)


def mocked_ecb_xml(*args, **kwargs):
    return MockResponseEcb('''<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" 
            xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
                <gesmes:subject>Reference rates</gesmes:subject>
                <gesmes:Sender>
                <gesmes:name>European Central Bank</gesmes:name>
                    </gesmes:Sender>
                        <Cube>
                            <Cube time="2020-11-26">
                            <Cube currency="USD" rate="1.600"/>
                            <Cube currency="JPY" rate="124.04"/>
                        </Cube>
                    </Cube>
                </gesmes:Envelope>''', 200)


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

    @patch('controllers.exchange_rates.requests.get',
           side_effect=mocked_open_exchange_rates)
    def test_exch_rates(self, m):
        rates = openexchangerates()
        self.assertEqual(rates, {
                "AUD": 1.471887,
                "GBP": 0.778172,
                "RUB": 64.13375
            })

    def test_exch_rates_fail(self):
        with self.assertRaises(ValueError):
            openexchangerates(base='ETH')

    @patch('controllers.exchange_rates.requests.get',
           side_effect=mocked_open_exchange_rates)
    def test_factor__exchange_success(self, m):

        f = self.bitfinex_resp.factor(('btcusd', 'BTC:RUB', openexchangerates))

        self.assertEqual(f, 64.13375)

    @patch('controllers.exchange_rates.requests.get',
           side_effect=mocked_open_exchange_rates)
    def test_factor__exchange_success_GBP(self, m):

        f = self.bitfinex_resp.factor(('btcgbp', 'BTC:GBP', openexchangerates))

        self.assertEqual(f, 0.778172)

    @patch('controllers.exchange_rates.requests.get', side_effect=mocked_ecb_xml)
    def test_ecb(self, m):
        ecb.delete_memoized()
        rates = ecb()
        self.assertEqual(rates, {'EUR': 0.625})
