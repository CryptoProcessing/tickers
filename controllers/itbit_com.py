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
    )

    def __init__(self, fund_ids=fund_ids):
        super(Itbit, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_ids:
            url = 'https://api.itbit.com/v1/markets/XBTUSD/ticker'

            req = requests.get(url)
            req_json = req.json()

            if not req_json:
                continue

            fund_data = {
                'ask': float(req_json['ask']),
                'bid': float(req_json['bid']),
                'date': self.str_to_date(req_json['serverTimeUTC']),
                'fund_id': self.map_fund(fund[0]),
            }

            data.append(fund_data)
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.strptime(strdate.rsplit('.', 1)[0], self.date_fmt)
        except ValueError:
            return datetime.datetime.now()


