# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now

from trade.get_price import get_current_ETH_price
from trade.models import EthereumPrice


@shared_task
def update_last_login_for_user(user_id):






    User.objects.filter(id=user_id).update(last_login=now())


@shared_task
def update_eth_price():
    get_current_ETH_price()

