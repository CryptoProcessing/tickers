from controllers.base_ticker import BaseTicker
from controllers.exchange_rates import openexchangerates


class Bisq(BaseTicker):
    """
    https://markets.bisq.network/api/ticker?market=btc_usd
    """

    date_fmt = ""

    # GGT  is token = 1$
    fund_ids = (
        ("btc_usd", "BTC:USD"),
        ("btc_usd", "BTC:GGT", 10),
        ("btc_eur", "BTC:EUR"),
        ("btc_gbp", "BTC:GBP"),
        ("btc_aud", "BTC:AUD"),
        ("btc_usd", "BTC:RUB", openexchangerates),
        ("eth_btc", "ETH:BTC"),
    )

    def __init__(self, fund_ids=fund_ids):
        super(Bisq, self).__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        data = []
        for fund in self.fund_id:
            url = "https://markets.bisq.network/api/ticker?market={}".format(fund[0])

            req_json = self.make_request(url)

            if not req_json:
                continue
            try:
                fund_data = {
                    "ask": float(req_json[0]["last"]) * self.factor(fund),
                    "bid": float(req_json[0]["last"]) * self.factor(fund),
                    "date": self.str_to_date(req_json[0].get("timestamp")),
                    "fund_id": fund[1],
                }

                data.append(fund_data)
            except KeyError:
                pass
        return data

    def str_to_date(self, strdate):
        return super(Bisq, self).str_to_date(strdate)
