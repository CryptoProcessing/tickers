from abc import ABCMeta, abstractmethod
from datetime import datetime


class BaseTicker(metaclass=ABCMeta):
    date_fmt = '%Y-%m-%dT%H:%M:%S.%f%z'

    fund_ids = (
        ('BTCUSD', 'BTC:USD'),
        ('ETHBTC', 'ETH:BTC'),
        ('ETHEUR', 'ETH:EUR')
    )

    def __init__(self, fund_ids=fund_ids, ):
        self.fund_id = fund_ids

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