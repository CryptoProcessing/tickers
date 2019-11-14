import requests
from flask import current_app


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
