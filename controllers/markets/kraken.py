import datetime
from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates, ecb


class Kraken(BaseTicker):
    """
    https://api.kraken.com/0/public/Ticker pair = через запятую, перечень валютных пар для получения данных
    https://api.kraken.com/0/public/AssetPairs
    """
    date_fmt = ''

    # GGT  is token = 10$
    fund_ids = (
        ('XBTUSDT', 'BTC:USD'),
        ('XXBTZGBP', 'BTC:GBP', ),
        ('XBTUSDT', 'BTC:RUB', openexchangerates),
        ('XBTAUD', 'BTC:AUD', ),
        ('XBTUSDT', 'BTC:GGT', 10),
        ('XETHXXBT', 'ETH:BTC'),
        ('XETHZUSD', 'ETH:USD'),
        ('XETHZUSD', 'ETH:GGT', 10),
        ('LTCUSDT', 'LTC:USD'),
        ('TRXXBT', 'TRX:BTC',),
        ('TRXUSD', 'TRX:USD',),
        ('TRXUSD', 'TRX:EUR', ecb),
        ('XBTUSDT', 'BTC:EUR', ecb),
        ('XBTDAI', 'BTC:DAI',),
        # ('ETHDAI', 'ETH:DAI',),
        ('XBTUSDC', 'BTC:USDC',),
        ('ETHUSDC', 'ETH:USDC',),
    )

    def __init__(self, fund_ids=fund_ids):
        super().__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = 'https://api.kraken.com/0/public/Ticker?pair={}'.format(fund[0])

            req_json = self.make_request(url)

            if not req_json:
                continue
            try:
                pair = req_json['result'][fund[0]]
                fund_data = {
                    'ask': float(pair['a'][0]) * self.factor(fund),
                    'bid': float(pair['b'][0]) * self.factor(fund),
                    'date': self.str_to_date(''),
                    'fund_id': fund[1],
                }

                data.append(fund_data)
            except KeyError:
                pass
        return data

    def str_to_date(self, strdate):
        """
        Get date from timestamp
        :param strdate:
        :return:
        """
        return datetime.datetime.now()



