import requests,decimal,json


def get_current_ETH_price():
    from trade.models import EthereumPrice

    # database'den cek son bir dakika icinde varsa, yoksa sorgu yap
    url = 'https://www.cryptocompare.com/api/data/price?fsym=ETH&tsyms=USD'
    response = requests.get(url)

    if response.status_code == 200:
        price = decimal.Decimal(json.loads(response.content)['Data'][0]['Price'])
        EthereumPrice.objects.create(price=price)
        return {'status': 'Success',
                'price': price}
    else:
        return {'status': 'Error', 'price': None }