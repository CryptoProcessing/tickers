import xml.etree.ElementTree as ET  # nosec

import requests
from flask import current_app

from ticker.extensions import cache


@cache.memoize(timeout=14000)  # 45 minutes
def openexchangerates(base: str = "BTC"):
    """

    :param base:
    :return:
    """
    if base != "BTC":
        raise ValueError

    url = "https://openexchangerates.org/api/latest.json?app_id={}"
    req = requests.get(url.format(current_app.config["OPENEXCHANGERATES_API_KEY"]), base)
    return req.json()["rates"]


@cache.memoize(timeout=14400)  # 4 часа
def ecb(base: str = ""):
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    req = requests.get(url)
    envelope = ET.fromstring(req.text)  # nosec

    namespaces = {
        "gesmes": "http://www.gesmes.org/xml/2002-08-01",
        "eurofxref": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref",
    }

    currency_elements = envelope.findall(
        "./eurofxref:Cube/eurofxref:Cube/eurofxref:Cube[@currency][@rate]", namespaces
    )
    rates = {}

    applicable_currenties = {"USD": True}

    for currency_element in currency_elements:
        code = currency_element.attrib.get("currency")

        if code not in applicable_currenties:
            continue

        rate = currency_element.attrib.get("rate")
        rates["EUR"] = 1 / float(rate)

    return rates
