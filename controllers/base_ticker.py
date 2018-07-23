import requests
from abc import ABCMeta, abstractmethod
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from flask import current_app


class BaseTicker(metaclass=ABCMeta):
    date_fmt = '%Y-%m-%dT%H:%M:%S.%f%z'

    # ((in_response, in_base, factor(not required)))
    fund_ids = (
        ('BTCUSD', 'BTC:USD'),
        ('ETHBTC', 'ETH:BTC'),
        ('ETHEUR', 'ETH:EUR')
    )

    def __init__(self, fund_ids=fund_ids, ):
        self.fund_id = fund_ids

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
    def make_request(self, url):
        req = requests.get(url, timeout=self._get_request_timeout())
        return req.json()

    @staticmethod
    def _get_request_timeout():
        return current_app.config.get('REQUEST_TIMEOUT', 5)

    def factor(self, fund):
        try:
            return int(fund[2])
        except (IndexError, ValueError):
            return 1

    @abstractmethod
    def get_ticker_info(self):
        pass

    def map_fund(self, fund_id):
        for f_id in self.fund_id:
            if f_id[0] == fund_id:
                return f_id[1]
        return None

    @abstractmethod
    def str_to_date(self, strdate):

        try:
            return datetime.strptime(''.join(strdate.rsplit(':', 1)), self.date_fmt)
        except (ValueError, AttributeError):
            return datetime.now()