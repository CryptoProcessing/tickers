from .base_ticker import BaseTicker
import requests
import datetime


class Cexio(BaseTicker):
    """
    https://cex.io/api/tickers/BTC/USD
    """

    # GGT  is token = 1$
    fund_ids = (
        ('BTC:USD', 'BTC:USD'),
        ('BTC:USD', 'BTC:GGT'),
        ('ETH:BTC', 'ETH:BTC'),
        ('ETH:USD', 'ETH:USD'),
        ('ETH:USD', 'ETH:GGT'),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Cexio, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://cex.io/api/tickers/BTC/USD'

        req = requests.get(url)
        req_json = req.json()

        data = []

        if not req_json:
            return []

        list_fund_id = [(f_id[0], f_id[1]) for f_id in self.fund_id]

        for lf in list_fund_id:
            fund_data =[
               {'ask': f['ask'],
                'bid': f['bid'],
                'date': self.str_to_date(f['timestamp']),
                'fund_id': lf[1],
                }
               for f in req_json['data'] if f['pair'] in [lf[0]]
           ]
            data.extend(fund_data)
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()


