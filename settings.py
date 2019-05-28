import os

TOKEN = os.environ.get('TOKEN')
SERVER_URL = 'https://free.currconv.com/api/v7'

CURRENCIES_URL = f'{SERVER_URL}/currencies'

assets_url = 'http://easyconvert.azurewebsites.net/api/currency/assets'
exchange_url = 'http://easyconvert.azurewebsites.net/api/currency/exchangerate/{0}/{1}'
support_id = 349671524
