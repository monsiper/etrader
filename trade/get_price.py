import requests,decimal,json

URL_ETH_PRICE = 'https://www.cryptocompare.com/api/data/price?fsym=ETH&tsyms=USD'

def get_current_ETH_price(url_eth_price):
    from trade.models import EthereumPrice

    # database'den cek son bir dakika icinde varsa, yoksa sorgu yap
    url = url_eth_price
    response = requests.get(url)

    if response.status_code == 200:
        price = decimal.Decimal(json.loads(response.content)['Data'][0]['Price'])
        EthereumPrice.objects.create(price=price)
        return {'status': 'Success',
                'price': price}
    else:
        return {'status': 'Error', 'price': None }