# coding=utf-8
import requests
from errors import *

from settings import exchange_url, assets_url


def get_asset_dictionary():
    assets = dict()
    try:
        request = requests.get(assets_url).json()

        for asset in request:
            assets[asset['assetId']] = {'name': asset['name'], 'is_crypto': asset['isTypeCrypto']}

        return assets
    except:
        return None


def get_rate(base, quote):
    try:
        result = requests.get(exchange_url.format(base, quote))
        data = result.json()
        return float(data['exchangeRate']['rate'])
    except ValueError as e:
        print(exchange_url.format(base, quote))
        print(e)
        return None


def parse_text(text, assets):
    separators = [' -> ', ' to ', ' - ', ' > ', ' в ']
    separator = ' '

    for s in separators:
        if s in text:
            separator = s

    data = text.rsplit(separator, 1)
    print(data)

    result = few_arguments
    if len(data) == 2:
        base = find_entry(data[0], assets)
        quote = find_entry(data[1], assets)

        if base[1] is None and quote[1] is None:
            print(base, quote)
            result = asset_not_found + "`{0}, {1}`".format(base[0][0], quote[0][0])
        elif base[1] is None:
            result = asset_not_found + "`{0}`".format(base[0][0])
        elif quote[1] is None:
            result = asset_not_found + "`{0}`".format(quote[0][0])
        elif base[1] == -1:
            result = left_asset_value_error + "`{0}`".format(data[0])
        else:
            result = base, quote

    return result


def find_entry(text, assets):
    left_asset = text.lower().split(' ')
    for asset_id, asset_info in assets.items():
        if asset_id.lower() == text.lower().strip():
            return asset_id, 1
        if len(left_asset) == 2 and asset_id.lower() == left_asset[1]:
            try:
                amount = float(left_asset[0])
            except ValueError:
                amount = -1
            return asset_id, amount
    return left_asset[1] if len(left_asset) == 2 else left_asset, None
