from .base_ticker import BaseTicker
import requests


class Therocktrading(BaseTicker):
    """
    https://api.therocktrading.com/v1/funds/tickers
    """
    fund_ids = (
        ('BTCUSD', 'BTC:USD'),
        ('ETHBTC', 'ETH:BTC'),
        ('ETHEUR', 'ETH:EUR')
    )

    def __init__(self, fund_ids=fund_ids):
        super(Therocktrading, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://api.therocktrading.com/v1/funds/tickers'

        req = requests.get(url)
        req_json = req.json()

        if not req_json:
            return []

        list_fund_id = [f_id[0] for f_id in self.fund_id]
        data =[
            {'ask': f['ask'],
             'bid': f['bid'],
             'date': self.str_to_date(f['date']),
             'fund_id':self.map_fund(f['fund_id']),
               }
            for f in req_json['tickers'] if f['fund_id'] in list_fund_id
        ]

        return data
    
    def str_to_date(self, strdate):
        return super(Therocktrading, self).str_to_date(strdate)


