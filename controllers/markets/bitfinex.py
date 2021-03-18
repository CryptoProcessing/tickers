import datetime
from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates


class Bitfinex(BaseTicker):
    """
    https://api.bitfinex.com/v1/pubticker/btcusd
    curl https://api-pub.bitfinex.com/v2/tickers?symbols=ALL

    """
    date_fmt = '%Y-%m-%dT%H:%M%S.%fZ'

    # GGT  is token = 1$
    fund_ids = (
        ('btcusd', 'BTC:USD'),
        ('btceur', 'BTC:EUR'),
        ('btcgbp', 'BTC:GBP'),
        ('btcusd', 'BTC:RUB', openexchangerates),
        ('btcusd', 'BTC:AUD', openexchangerates),
        ('ethbtc', 'ETH:BTC'),
        ('btcusd', 'BTC:GGT', 10),
        ('ethusd', 'ETH:USD'),
        ('ethusd', 'ETH:GGT', 10),
        ('ltcusd', 'LTC:USD'),  # Litecoin
        # ('bchusd', 'BCH:USD'),  # Bitcoin Cash / BCC
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitfinex, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.bitfinex.com/v1/pubticker/{}'.format(fund[0])

            req_json = self.make_request(url)

            if not req_json:
                continue
            try:
                fund_data = {
                    'ask': float(req_json['ask']) * self.factor(fund),
                    'bid': float(req_json['bid']) * self.factor(fund),
                    'date': self.str_to_date(req_json['timestamp']),
                    'fund_id': fund[1],
                }
                data.append(fund_data)
            except KeyError:
                pass

        return data

    def str_to_date(self, strdate):
        try:
            return datetime.datetime.utcfromtimestamp(float(strdate))
        except ValueError:
            return datetime.datetime.utcnow()


