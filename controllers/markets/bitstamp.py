from controllers.base_ticker import BaseTicker
import requests
import datetime


class Bitstamp(BaseTicker):
    """
    https://www.bitstamp.net/api/v2/ticker/{currency_pair}/
    https://www.bitstamp.net/api/v2/trading-pairs-info/
    """
    date_fmt = ''

    # GGT  is token = 10$
    fund_ids = (
        ('btcusd', 'BTC:USD'),
        ('btcusd', 'BTC:GGT', 10),
        ('ethbtc', 'ETH:BTC'),
        ('ethusd', 'ETH:USD'),
        ('ethusd', 'ETH:GGT', 10),
        ('ltcusd', 'LTC:USD'),
        ('bchusd', 'BCH:USD'),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitstamp, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://www.bitstamp.net/api/v2/ticker/{}/'.format(fund[0])

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': float(req_json['ask']) * self.factor(fund),
                'bid': float(req_json['bid']) * self.factor(fund),
                'date': self.str_to_date(req_json.get('timestamp')),
                'fund_id': fund[1],
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        """
        Get date from timestamp
        :param strdate:
        :return:
        """
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()



