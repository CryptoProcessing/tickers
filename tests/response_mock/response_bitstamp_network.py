from datetime import datetime

expected_response = [
    {'ask': 7541.86,
     'bid': 7538.88,
     'date': datetime(2018, 5, 31, 13, 58, 17),
     'fund_id': 'BTC:USD'},
    {'ask': 0.07575115,
     'bid': 0.07562026,
     'date': datetime(2018,  5, 31, 13, 57, 2),
     'fund_id': 'ETH:BTC'}
]

response_btc_usd = {
        "high": "7599.99",
        "last": "7538.88",
        "timestamp": "1527764297",
        "bid": "7538.88",
        "vwap": "7431.88",
        "volume": "8716.27046671",
        "low": "7273.89",
        "ask": "7541.86",
        "open": "7375.64"
    }

response_eth_btc =  {
        "high": "0.07683000",
        "last": "0.07554523",
        "timestamp": "1527764222",
        "bid": "0.07562026",
        "vwap": "0.07561960",
        "volume": "3282.48128789",
        "low": "0.07418408",
        "ask": "0.07575115",
        "open": "0.07566000"
    }
