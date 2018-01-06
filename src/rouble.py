#!/usr/bin/env python
# coding:utf-8

import json
import urllib2
import os
import time
import locale
import sys
from settings_local import __apikey__
from collections import OrderedDict

__author__ = 'hewigovens'
__version__ = '1.0.1'

latest_rates = 'latest_rates.json'
popclip_text = os.getenv('POPCLIP_TEXT')
popclip_text = popclip_text.replace(',', '')
support_currency = OrderedDict([
    ('USD', 'USD'),
    ('$', 'USD'),
    ('£', 'GBP'),
    ('€', 'EUR'),
    ('JPY', 'JPY'),
    ('￥', 'JPY')
])

#locale.setlocale(locale.LC_ALL, 'en_US')
fp = None
dollars = None


def get_latest_rates():
    rates_req = urllib2.urlopen(
        'https://openexchangerates.org/api/latest.json?app_id=%s' % __apikey__)
    with open(latest_rates, 'w') as fp:
        fp.writelines(''.join(rates_req.readlines()))


def main():
    if not os.path.exists(latest_rates):
        get_latest_rates()

    time_now = int(time.time())
    timestamp = sys.maxint
    try:
        fp = open(latest_rates)
        rates_json = json.load(fp)
        timestamp = rates_json['timestamp']
    except:
        pass
    finally:
        if time_now - timestamp >= 3600:
            fp.close()
            get_latest_rates()
            fp = open(latest_rates)
            rates_json = json.load(fp)

    for currency in support_currency.keys():
        if currency in popclip_text:
            dollars = float(popclip_text.replace(
                currency, '').replace(' ', '')) / rates_json['rates'][support_currency[currency]]
            break

    rouble = dollars * rates_json['rates']['RUB']

    print("%s₽" % (locale.format('%.2f', rouble, grouping=True)))
    fp.close

if __name__ == '__main__':
    main()
