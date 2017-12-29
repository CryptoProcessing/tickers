import datetime


######### bitfinex #########
bitfinex_response_btc_usd = {
    "mid": "13132.0",
    "bid": "13130.0",
    "ask": "13134.0",
    "last_price": "13124.12229096",
    "low": "11600.0",
    "high": "14999.0",
    "volume": "75271.49638604",
    "timestamp": "1514127458.4666939"
}
bitfinex_response_eth_btc = {
    "mid": "0.0513485",
    "bid": "0.051348",
    "ask": "0.051349",
    "last_price": "0.051349",
    "low": "0.049047",
    "high": "0.051584",
    "volume": "74071.6467398",
    "timestamp": "1514558930.472265"
}


bitfinex_expected_response =[
    {'fund_id': 'BTC:USD',
     'date':  datetime.datetime(2017, 12, 24, 17, 57, 38, 466694),
     'ask': '13134.0',
     'bid': '13130.0'},
    {'fund_id': 'ETH:BTC',
     'date': datetime.datetime(2017, 12, 29, 17, 48, 50, 472265),
     'bid': '0.051348',
     'ask': '0.051349'}
]
######### GDAX #########

gdax_response_eth_btc = {
    "trade_id": 2804134,
    "price": "0.04680000",
    "size": "4.12828010",
    "bid": "0.04678",
    "ask": "0.04679",
    "volume": "76442.41371020",
    "time": "2017-12-20T13:04:34.183000Z"
}


gdax_response_btc_usd = {
    "trade_id": 29190839,
    "price": "17698.86000000",
    "size": "0.06313891",
    "bid": "17698.86",
    "ask": "17698.87",
    "volume": "49392.47063037",
    "time": "2017-12-20T13:22:52.613000Z"
}


gdax_expected_response =[
    {'fund_id': 'BTC:USD',
     'date': datetime.datetime(2017, 12, 20, 13, 22, 52, 613000),
     'ask': '17698.87',
     'bid': '17698.86'},
    {'fund_id': 'ETH:BTC',
     'date': datetime.datetime(2017, 12, 20, 13, 4, 34, 183000),
     'ask': '0.04679',
     'bid': '0.04678'}
]


######### the rock #########

therock_response = {
    "tickers": [
        {
            "date": "2017-12-18T16:24:30.152+01:00",
            "fund_id": "BTCEUR",
            "bid": 15689.23,
            "ask": 15754.83,
            "last": 15689.23,
            "open": 15923.83,
            "close": 16014,
            "low": 15610,
            "high": 16621.99,
            "volume": 2697628.95,
            "volume_traded": 197.511
        },
        {
            "date": "2017-12-18T16:25:34.887+01:00",
            "fund_id": "BTCUSD",
            "bid": 18000.01,
            "ask": 19898.84,
            "last": 18900,
            "open": 19000,
            "close": 19999.99,
            "low": 19000,
            "high": 19999.99,
            "volume": 14339.62,
            "volume_traded": 0.759
        },
        {
            "date": "2017-12-18T16:25:37.428+01:00",
            "fund_id": "LTCEUR",
            "bid": 260.3,
            "ask": 265.5,
            "last": 264.67,
            "open": 252.9,
            "close": 265.64,
            "low": 249,
            "high": 269.99,
            "volume": 295486.38,
            "volume_traded": 1123.87
        },
        {
            "date": "2017-12-18T16:22:46.389+01:00",
            "fund_id": "LTCBTC",
            "bid": 0.01679,
            "ask": 0.017,
            "last": 0.0168,
            "open": 0.0154,
            "close": 0.0166,
            "low": 0.0154,
            "high": 0.01708,
            "volume": 7.14387129,
            "volume_traded": 427.05
        },
        {
            "date": "2017-12-18T16:25:35.219+01:00",
            "fund_id": "BTCXRP",
            "bid": 25886.61,
            "ask": 26441.02,
            "last": 25740.02,
            "open": 26143.78,
            "close": 25900.02,
            "low": 25233.4,
            "high": 28184.89,
            "volume": 92555.69062,
            "volume_traded": 3.491
        },
        {
            "date": "2017-12-18T16:25:28.737+01:00",
            "fund_id": "EURXRP",
            "bid": 1.61,
            "ask": 1.66,
            "last": 1.62,
            "open": 1.59,
            "close": 1.65,
            "low": 1.58,
            "high": 1.72,
            "volume": 159446.2838,
            "volume_traded": 95380.05
        },
        {
            "date": "2017-12-18T16:25:35.200+01:00",
            "fund_id": "USDXRP",
            "bid": 1.36,
            "ask": 1.4,
            "last": 1.39,
            "open": 1.35,
            "close": 1.38,
            "low": 1.34,
            "high": 1.4,
            "volume": 3763.3434,
            "volume_traded": 2650.54
        },
        {
            "date": "2017-12-18T15:24:59.110+00:00",
            "fund_id": "PPCEUR",
            "bid": 5.08,
            "ask": 5.13,
            "last": 5.08,
            "open": 4.82,
            "close": 5.27,
            "low": 4.71,
            "high": 5.35,
            "volume": 41941.78,
            "volume_traded": 8088.74
        },
        {
            "date": "2017-12-18T16:17:10.551+01:00",
            "fund_id": "PPCBTC",
            "bid": 0.0003,
            "ask": 0.00033,
            "last": 0.0003,
            "open": 0.00031,
            "close": 0.00033,
            "low": 0.00029,
            "high": 0.00035,
            "volume": 0.71582807,
            "volume_traded": 2209.04
        },
        {
            "date": "2017-12-18T16:25:01.155+01:00",
            "fund_id": "ETHEUR",
            "bid": 592.01,
            "ask": 600,
            "last": 599,
            "open": 565,
            "close": 590.74,
            "low": 565,
            "high": 609.99,
            "volume": 492466.45,
            "volume_traded": 908.4
        },
        {
            "date": "2017-12-18T16:25:34.205+01:00",
            "fund_id": "ETHBTC",
            "bid": 0.03831,
            "ask": 0.03875,
            "last": 0.03836,
            "open": 0.03564,
            "close": 0.0374,
            "low": 0.03564,
            "high": 0.03843,
            "volume": 11.81984046,
            "volume_traded": 313.64
        },
        {
            "date": "2017-12-18T16:17:21.495+01:00",
            "fund_id": "ZECBTC",
            "bid": 0.02796,
            "ask": 0.0281,
            "last": 0.02801,
            "open": 0.02399,
            "close": 0.02768,
            "low": 0.02399,
            "high": 0.0288,
            "volume": 1.618766,
            "volume_traded": 58.855
        },
        {
            "date": "2017-12-18T16:18:53.816+01:00",
            "fund_id": "ZECEUR",
            "bid": 436.71,
            "ask": 439,
            "last": 432.51,
            "open": 387.23,
            "close": 439.15,
            "low": 383.6,
            "high": 459.82,
            "volume": 108835.1,
            "volume_traded": 249.578
        },
        {
            "date": "2017-12-18T16:25:38.770+01:00",
            "fund_id": "BCHBTC",
            "bid": 0.10844,
            "ask": 0.10944,
            "last": 0.10843,
            "open": 0.09281,
            "close": 0.09691,
            "low": 0.09109,
            "high": 0.09865,
            "volume": 6.61194998,
            "volume_traded": 62.574
        },
        {
            "date": "2017-12-18T15:24:54.520+00:00",
            "fund_id": "EURNEUR",
            "bid": 1.01,
            "ask": 1.02,
            "last": 1.02,
            "open": 1.01,
            "close": 1.02,
            "low": 0.99,
            "high": 1.02,
            "volume": 27950.56,
            "volume_traded": 27433.31
        },
        {
            "date": "2017-12-18T15:25:15.187+00:00",
            "fund_id": "EURNBTC",
            "bid": 0.00006,
            "ask": 0.00007,
            "last": 0.00007,
            "open": 0.00006,
            "close": 0.00006,
            "low": 0.00006,
            "high": 0.00006,
            "volume": 0.02035,
            "volume_traded": 305
        }
    ]
}

therock_expected_response = [
    {
        'bid': 18000.01,
        'date': datetime.datetime(2017, 12, 18, 16, 25, 34, 887000, tzinfo=datetime.timezone(datetime.timedelta(0, 3600))),
        'fund_id': 'BTC:USD',
        'ask': 19898.84
    },
    {
        'bid': 0.03831,
        'date':  datetime.datetime(2017, 12, 18, 16, 25, 34, 205000, tzinfo=datetime.timezone(datetime.timedelta(0, 3600))),
        'fund_id':
            'ETH:BTC',
        'ask': 0.03875
    }
]
