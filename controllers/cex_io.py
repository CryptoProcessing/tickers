from .base_ticker import BaseTicker
import requests
import datetime


class Cexio(BaseTicker):
    """
    https://cex.io/api/tickers/BTC/USD
    """
    fund_ids = (
        ('BTC:USD', 'BTC:USD'),
        ('ETH:BTC', 'ETH:BTC'),
        ('ETH:USD', 'ETH:USD')
    )

    def __init__(self, fund_ids=fund_ids):
        super(Cexio, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://cex.io/api/tickers/BTC/USD'

        req = requests.get(url)
        req_json = req.json()

        if not req_json:
            return []

        list_fund_id = [f_id[0] for f_id in self.fund_id]
        data = [
            {'ask': f['ask'],
             'bid': f['bid'],
             'date': self.str_to_date(f['timestamp']),
             'fund_id': self.map_fund(f['pair']),
             }
            for f in req_json['data'] if f['pair'] in list_fund_id
        ]

        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()


