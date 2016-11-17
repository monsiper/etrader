import requests,decimal,json

def get_current_ETH_price():

    url = 'https://www.cryptocompare.com/api/data/price?fsym=ETH&tsyms=USD'
    response = requests.get(url)

    if response.status_code == 200:
        return {'status': 'Success',
                'price': decimal.Decimal(json.loads(response.content)['Data'][0]['Price'])}
    else:
        return {'status': 'Error', 'price': None }