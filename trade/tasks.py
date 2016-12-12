# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now
from trade.ETH_price import get_price_from_web_api
from trade.models import URL_ETH_PRICE


@shared_task
def update_last_login_for_user(user_id):
    User.objects.filter(id=user_id).update(last_login=now())


# @shared_task
# def update_eth_price():
#     get_price_from_web_api(URL_ETH_PRICE)
#
