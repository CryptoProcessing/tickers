import datetime

bitsmap_expected_response = [
    {'ask': 8194.56,
     'bid': 8187.77,
     'date': datetime.datetime(2018, 2, 9, 15, 25, 32),
     'fund_id': 'BTC:USD'},
    {'ask': 825.54,
     'bid': 822.00,
     'date': datetime.datetime(2018, 2, 9, 15, 25, 33),
     'fund_id': 'ETH:USD'}
]

bitsmap_response_btc_usd = {
    "high": "8644.36",
    "last": "8187.77",
    "timestamp": "1518179132",
    "bid": "8187.77",
    "vwap": "8160.42",
    "volume": "22451.37455985",
    "low": "7753.32",
    "ask": "8194.56",
    "open": "8259.42"
}

bitsmap_response_eth_usd = {
    "high": "839.00",
    "last": "822.00",
    "timestamp": "1518179133",
    "bid": "822.00",
    "vwap": "806.19",
    "volume": "41171.24690470",
    "low": "780.88",
    "ask": "825.54",
    "open": "814.32"
}