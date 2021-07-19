from controllers.base_ticker import BaseTicker


class Binance(BaseTicker):
    """
    https://api.binance.com/api/v3/ticker/bookTicker
    """

    # GGT  is token = 1$
    fund_ids = (
        (
            "BTCUSDT",
            "BTC:USD",
        ),
        (
            "ETHUSDT",
            "ETH:USD",
        ),
        (
            "BNBUSDT",
            "BNB:USD",
        ),
        (
            "LTCUSDT",
            "LTC:USD",
        ),
        (
            "TRXUSDT",
            "TRX:USD",
        ),
    )

    def __init__(self, fund_ids=fund_ids):
        super().__init__()
        self.fund_id = fund_ids

    def get_ticker_info(self):
        url = "https://api.binance.com/api/v3/ticker/bookTicker"

        req_json = self.make_request(url)

        if not req_json:
            return []

        data = []
        list_fund_id = [f_id for f_id in self.fund_id]

        for lf in list_fund_id:
            try:
                fund_data = [
                    {
                        "ask": float(f["askPrice"]) * self.factor(lf),
                        "bid": float(f["bidPrice"]) * self.factor(lf),
                        "date": self.str_to_date(strdate=""),
                        "fund_id": lf[1],
                    }
                    for f in req_json
                    if f["symbol"] in [lf[0]]
                ]
                data.extend(fund_data)
            except KeyError:
                pass
        return data

    def str_to_date(self, strdate):
        return super().str_to_date(strdate)
