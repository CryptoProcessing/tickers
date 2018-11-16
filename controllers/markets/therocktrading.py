from controllers.base_ticker import BaseTicker
import requests


class Therocktrading(BaseTicker):
    """
    https://api.therocktrading.com/v1/funds/tickers
    """

    # GGT  is token = 1$
    fund_ids = (
        ('BTCUSD', 'BTC:USD',),
        ('BTCUSD', 'BTC:GGT', 10),

        ('ETHBTC', 'ETH:BTC',),
        ('ETHEUR', 'ETH:EUR',)
    )

    def __init__(self, fund_ids=fund_ids):
        super(Therocktrading, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://api.therocktrading.com/v1/funds/tickers'

        req_json = self.make_request(url)

        if not req_json:
            return []

        data = []
        list_fund_id = [f_id for f_id in self.fund_id]

        for lf in list_fund_id:
            try:
                fund_data = [
                    {'ask': f['ask'] * self.factor(lf),
                     'bid': f['bid'] * self.factor(lf),
                     'date': self.str_to_date(f['date']),
                     'fund_id':lf[1],
                       }
                    for f in req_json['tickers'] if f['fund_id'] in [lf[0]]
                ]

                data.extend(fund_data)
            except KeyError:
                pass
        return data
    
    def str_to_date(self, strdate):
        return super(Therocktrading, self).str_to_date(strdate)


