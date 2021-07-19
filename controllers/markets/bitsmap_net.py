import datetime

from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates


class Bitsmap(BaseTicker):
    """
    https://www.bitstamp.net/api/v2/ticker/ethbtc
    """

    date_fmt = "%Y-%m-%dT%H:%M%S.%fZ"

    # GGT  is token = 1$
    fund_ids = (
        ("btcusd", "BTC:USD"),
        ("btceur", "BTC:EUR"),
        ("btcusd", "BTC:RUB", openexchangerates),
        ("btcusd", "BTC:AUD", openexchangerates),
        ("btcusd", "BTC:GGT", 10),
        ("ethusd", "ETH:GGT", 10),
        ("ethbtc", "ETH:BTC"),
        ("ethusd", "ETH:USD"),
        ("ltcusd", "LTC:USD"),
        # ('bchusd', 'BCH:USD'), # Bitcoin Cash / BCC
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bitsmap, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = "https://www.bitstamp.net/api/v2/ticker/{}".format(fund[0])

            req_json = self.make_request(url)

            if not req_json:
                continue
            try:
                fund_data = {
                    "ask": float(req_json["ask"]) * self.factor(fund),
                    "bid": float(req_json["bid"]) * self.factor(fund),
                    "date": self.str_to_date(req_json["timestamp"]),
                    "fund_id": fund[1],
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
