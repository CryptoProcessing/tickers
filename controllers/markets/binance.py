from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates, ecb


class Binance(BaseTicker):
    """
    https://api.binance.com/api/v3/ticker/bookTicker
    """

    # GGT  is token = 1$
    fund_ids = (
        ('BTCUSDT', 'BTC:USD',),
        ('BTCRUB', 'BTC:RUB',),
        ('BTCGBP', 'BTC:GBP', ),
        ('BTCAUD', 'BTC:AUD', ),
        ('BTCUSDT', 'BTC:GGT', 10),
        ('ETHBTC', 'ETH:BTC',),
        ('ETHEUR', 'ETH:EUR',),
        ('TRXBTC', 'TRX:BTC',),
        ('TRXUSDT', 'TRX:USD',),
        ('TRXUSDT', 'TRX:EUR', ecb),
        ('BTCUSDT', 'BTC:EUR', ecb),
        ('ETHUSDT', 'ETH:EUR', ecb),
        ('BTCDAI', 'BTC:DAI',),
        # ('ETHDAI', 'ETH:DAI',),
        ('BTCUSDC', 'BTC:USDC',),
        ('ETHUSDC', 'ETH:USDC',),

    )

    def __init__(self, fund_ids=fund_ids):
        super().__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = 'https://api.binance.com/api/v3/ticker/bookTicker'

        req_json = self.make_request(url)

        if not req_json:
            return []

        data = []
        list_fund_id = [f_id for f_id in self.fund_id]

        for lf in list_fund_id:
            try:
                fund_data = [
                    {'ask': float(f['askPrice']) * self.factor(lf),
                     'bid': float(f['bidPrice']) * self.factor(lf),
                     'date': self.str_to_date(strdate=''),
                     'fund_id':lf[1],
                       }
                    for f in req_json if f['symbol'] in [lf[0]]
                ]
                data.extend(fund_data)
            except KeyError:
                pass
        return data
    
    def str_to_date(self, strdate):
        return super().str_to_date(strdate)


