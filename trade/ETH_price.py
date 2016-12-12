import requests,decimal,json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone


def get_price_from_web_api(api_url):
    url = api_url
    response = requests.get(url)

    if response.status_code == 200:
        price = decimal.Decimal(json.loads(response.content)['Data'][0]['Price'])
        return ('Success', price)
    else:
        return ('Error', None)


# class EthereumPriceManager(models.Manager):
#
#     def get_price_from_web_api(self, api_url):
#
#         url = api_url
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             price = decimal.Decimal(json.loads(response.content)['Data'][0]['Price'])
#             self.create(price=price)
#             return ('Success', price)
#         else:
#             return ('Error', None)


    # def get_current_ETH_price(self, price_url):
    #     # database'den cek son bir dakika icinde varsa, yoksa sorgu yap
    #     price_check_time = timezone.now() + relativedelta(seconds=-60)
    #     prices = self.filter(date_created__gte=price_check_time).order_by('-date_created')
    #
    #     if not prices:
    #         return self.get_price_from_web_api(price_url)
    #     else:
    #         return ('Success', prices[0].price)

#
# class EthereumPrice(models.Model):
#     objects = EthereumPriceManager()
#     price = models.DecimalField(max_digits=40, decimal_places=30)
#     date_created = models.DateTimeField(auto_now_add=True)


