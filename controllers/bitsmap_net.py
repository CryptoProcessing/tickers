from .base_ticker import BaseTicker
import requests
import datetime


class Bitsmap(BaseTicker):
    """
    https://www.bitstamp.net/api/v2/ticker/ethbtc
    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    fund_ids = (
        ('btcusd', 'BTC:USD'),
        ('ethbtc', 'ETH:BTC'),
        ('ethusd', 'ETH:USD')
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitsmap, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_ids:
            url = 'https://www.bitstamp.net/api/v2/ticker/{}'.format(fund[0])

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': float(req_json['ask']),
                'bid': float(req_json['bid']),
                'date': self.str_to_date(req_json['timestamp']),
                'fund_id': self.map_fund(fund[0]),
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()


