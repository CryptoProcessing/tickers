from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates


class Gdax(BaseTicker):
    """
    https://api.gdax.com/products/BTC-USD/ticker
    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    # GGT  is token = 1$
    fund_ids = (
        ('BTC-USD', 'BTC:USD'),
        ('BTC-EUR', 'BTC:EUR'),
        ('BTC-GBP', 'BTC:GBP'),
        ('BTC-USD', 'BTC:RUB', openexchangerates),
        ('BTC-USD', 'BTC:AUD', openexchangerates),
        ('BTC-USD', 'BTC:GGT', 10),
        ('ETH-BTC', 'ETH:BTC'),
        ('ETH-USD', 'ETH:USD'),
        ('ETH-USD', 'ETH:GGT', 10),
        ('LTC-USD', 'LTC:USD'),
        # ('BCH-USD', 'BCH:USD'), # Bitcoin Cash / BCC
    )

    def __init__(self, fund_ids=fund_ids):
        super(Gdax, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.gdax.com/products/{}/ticker'.format(fund[0])

            req_json = self.make_request(url)

            if not req_json:
                continue
            try:

                fund_data = {
                    'ask': float(req_json['ask']) * self.factor(fund),
                    'bid': float(req_json['bid']) * self.factor(fund),
                    'date': self.str_to_date(req_json['time']),
                    'fund_id': fund[1],
                }

                data.append(fund_data)
            except KeyError:
                pass
        return data

    def str_to_date(self, strdate):
        return super(Gdax, self).str_to_date(strdate)


