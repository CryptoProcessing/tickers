import requests
from flask import current_app
from ticker.extensions import cache


@cache.memoize(timeout=2700)  # 45 minutes
def openexchangerates(base: str = 'BTC'):
    """

    :param base:
    :return:
    """
    if base != 'BTC':
        raise ValueError

    url = 'https://openexchangerates.org/api/latest.json?app_id={}'
    req = requests.get(url.format(
        current_app.config['OPENEXCHANGERATES_API_KEY']),
        base
    )
    return req.json()['rates']
