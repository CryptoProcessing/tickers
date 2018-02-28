from .base_ticker import BaseTicker
import requests
import datetime


class Bitfinex(BaseTicker):
    """
    https://api.bitfinex.com/v1/pubticker/btcusd
    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    # GGT  is token = 1$
    fund_ids = (
        ('btcusd', 'BTC:USD'),
        ('ethbtc', 'ETH:BTC'),
        ('btcusd', 'BTC:GGT'),
        ('ethusd', 'ETH:USD'),
        ('ethusd', 'ETH:GGT')
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitfinex, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.bitfinex.com/v1/pubticker/{}'.format(fund[0])

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': req_json['ask'],
                'bid': req_json['bid'],
                'date': self.str_to_date(req_json['timestamp']),
                'fund_id': fund[1],
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()


