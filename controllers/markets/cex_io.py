from controllers.base_ticker import BaseTicker
import datetime


class Cexio(BaseTicker):
    """
    https://cex.io/api/tickers/BTC/USD
    """

    # GGT  is token = 1$
    fund_ids = (
        ('BTC:USD', 'BTC:USD'),
        ('ETH:USD', 'ETH:USD'),
        ('LTC:USD', 'LTC:USD'),
        ('TRX:USD', 'TRX:USD'),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Cexio, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://cex.io/api/tickers/BTC/USD/GBP/EUR'

        req_json = self.make_request(url)

        if not req_json:
            return []

        data = []

        list_fund_id = [f_id for f_id in self.fund_id]

        for lf in list_fund_id:
            try:
                fund_data =[
                   {'ask': float(f['ask']) * self.factor(lf),
                    'bid': float(f['bid']) * self.factor(lf),
                    'date': self.str_to_date(f['timestamp']),
                    'fund_id': lf[1],
                    }
                   for f in req_json['data'] if f['pair'] in [lf[0]]
               ]
                data.extend(fund_data)
            except KeyError:
                pass
        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.fromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.now()


