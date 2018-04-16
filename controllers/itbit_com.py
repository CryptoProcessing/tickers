from .base_ticker import BaseTicker
import requests
import datetime


class Itbit(BaseTicker):
    """
    https://api.itbit.com/v1/markets/XBTUSD/ticker
    """
    # "serverTimeUTC": "2018-02-14T20:34:24.4785988Z"
    date_fmt = '%Y-%m-%dT%H:%M:%S'

    fund_ids = (
        ('XBTUSD', 'BTC:USD'),
        ('XBTUSD', 'BTC:GGT', 1000),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Itbit, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.itbit.com/v1/markets/XBTUSD/ticker'

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': float(req_json['ask']) * self.factor(fund),
                'bid': float(req_json['bid']) * self.factor(fund),
                'date': self.str_to_date(req_json['serverTimeUTC']),
                'fund_id': fund[1],
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.strptime(strdate.rsplit('.', 1)[0], self.date_fmt)
        except ValueError:
            return datetime.datetime.now()


