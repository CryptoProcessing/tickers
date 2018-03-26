from .base_ticker import BaseTicker
import requests


class Gdax(BaseTicker):
    """
    https://api.gdax.com/products/BTC-USD/ticker
    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    # GGT  is token = 1$
    fund_ids = (
        ('BTC-USD', 'BTC:USD'),
        ('BTC-USD', 'BTC:GGT'),
        ('ETH-BTC', 'ETH:BTC'),
        ('ETH-USD', 'ETH:USD'),
        ('ETH-USD', 'ETH:GGT'),
        ('LTC-USD', 'LTC:USD'),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Gdax, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.gdax.com/products/{}/ticker'.format(fund[0])

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': req_json['ask'],
                'bid': req_json['bid'],
                'date': self.str_to_date(req_json['time']),
                'fund_id': fund[1],
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        return super(Gdax, self).str_to_date(strdate)


