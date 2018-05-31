from datetime import datetime

expected_response = [
    {'ask': 9468.36000000,
     'bid': 9468.36000000,
     'date': datetime.now(),
     'fund_id': 'BTC:USD'},
    {'ask': 0.10184646,
     'bid': 0.10184646,
     'date': datetime.now(),
     'fund_id': 'ETH:BTC'}
]

response_btc_usd = [
    { "last": "9468.36000000",
      "high": "9468.36000000",
      "low": "9224.21000000",
      "volume_left": "0.61700000",
      "volume_right": "5742.99440000",
      "buy": "9618.16000000",
      "sell": None }
]

response_eth_btc = [
    { "last": "0.10184646",
      "high": "0.10184646",
      "low": "0.10184646",
      "volume_left": 0,
      "volume_right": 0,
      "buy": None,
      "sell": None }
]