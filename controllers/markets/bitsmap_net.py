from controllers.base_ticker import BaseTicker
import requests
import datetime


class Bitsmap(BaseTicker):
    """
    https://www.bitstamp.net/api/v2/ticker/ethbtc
    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    # GGT  is token = 1$
    fund_ids = (
        ('btcusd', 'BTC:USD'),
        ('btcusd', 'BTC:GGT', 10),
        ('ethusd', 'ETH:GGT', 10),
        ('ethbtc', 'ETH:BTC'),
        ('ethusd', 'ETH:USD'),
        ('ltcusd', 'LTC:USD'),
        ('bchusd', 'BCH:USD'), # Bitcoin Cash / BCC
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitsmap, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://www.bitstamp.net/api/v2/ticker/{}'.format(fund[0])

            req = requests.get(url, timeout=2)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': float(req_json['ask']) * self.factor(fund),
                'bid': float(req_json['bid']) * self.factor(fund),
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


