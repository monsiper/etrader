from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
import decimal,logging
from get_price import get_current_ETH_price
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your models here.


logger = logging.getLogger(__name__)

class AccountManager(models.Manager):

    def create_account_for_user(self, user):

        try:
            Account.objects.get(user=user)
            return None

        except Account.DoesNotExist:
            return self.create(user=user, cash=decimal.Decimal(10000.00), coin=decimal.Decimal(0.00))


@receiver(post_save, sender=User)
def create_account(instance, created, **kwargs):
    if created:
        Account.objects.create_account_for_user(instance)


# user.account
# account.user

class Account(models.Model):
    objects = AccountManager()
    cash = models.DecimalField(max_digits=7, decimal_places=2)
    coin = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    buy_limit = models.DecimalField(max_digits=7, decimal_places=2, default=1000)
    sell_limit = models.DecimalField(max_digits=7, decimal_places=2, default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp_latest_activity = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    processing_lock = models.BooleanField(default=False)

    def is_daily_limit_exceeded(self, order):

        start_date = datetime.today()

        if order.type == 'Buy':
            list_of_orders = Order.objects.filter(user=self.user, order_status='Success',
                                                  type='Buy', last_updated_at__date=start_date).values_list('amount',flat=True)

            if sum(list_of_orders)+order.amount > self.buy_limit:
                return True
            else:
                return False

        else:
            list_of_orders = Order.objects.filter(user=self.user, order_status='Success',
                                                  type='Sell', last_updated_at__date=start_date).values_list('amount',flat=True)

            if sum(list_of_orders)+order.amount > self.sell_limit:
                return True
            else:
                return False

    def has_enough_cash_or_coin_for_order(self, order):

        if order.type == 'Buy':
            coin_price = get_current_ETH_price()

            if order.amount*coin_price['price'] > self.cash:
                return False
            else:
                return True
        else:

            if order.amount > self.coin:
                return False
            else:
                return True



class OrderManager(models.Manager):

    def place_order_for_user(self, user, type, amount):

        if user.account.is_active:
            return self.create(user=user, type=type, amount=decimal.Decimal(amount))
        else:
            return None

    def get_past_orders_for_user(self, user, status, timeframe):

        if timeframe == 'WEEK':
            start_date = datetime.today() + relativedelta(days=-7)
        elif timeframe == 'MONTH':
            start_date = datetime.today() + relativedelta(months=-1)
        elif timeframe == 'YEAR':
            start_date = datetime.today() + relativedelta(years=-1)
        else:
            return None

        if status == 'All':
            list_of_orders = Order.objects.filter(user=user, order_status__in=['Success','Fail'],
                                              last_updated_at__date__gte=start_date).\
                                            order_by('last_updated_at').values('type','amount','order_status')
        elif status == 'Success' or status == 'Fail':
            list_of_orders = Order.objects.filter(user=user, order_status=status,
                                              last_updated_at__date__gte=start_date).\
                                            order_by('last_updated_at').values('type','amount','order_status')
        else:
            return None

        if list_of_orders:
            return list_of_orders
        else:
            return None


class Order(models.Model):

    ORDER_TYPE_CHOICES = (('Buy','BUY'), ('Sell','SELL'))

    ORDER_STATUS_CHOICES = (('Pending', 'Order is pending'),
                            ('Success', 'Order has executed'),
                            ('Fail','Order has failed'))

    objects = OrderManager()
    type = models.CharField(choices=ORDER_TYPE_CHOICES, blank=False, max_length=10)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, default='Pending', max_length=10)
    placed_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
    # history = models.JSONField()

    def is_valid(self):

        if self.order_status == 'Pending':
            account = self.user.account
            return (not account.is_daily_limit_exceeded(self)) and account.has_enough_cash_or_coin_for_order(self)
        else:
            return None


    def change_order_status(self, new_status):

        if new_status in ['Pending', 'Success', 'Fail'] and self.order_status != new_status:

            self.order_status = new_status
            self.last_updated_at = timezone.now()
            self.save(update_fields=['order_status','last_updated_at'])
            return True
        else:
            return False


    def cancel_order(self):

        if self.order_status == 'Pending':
            self.order_status = 'Fail'
            self.last_updated_at = timezone.now()
            self.save(update_fields=['order_status','last_updated_at'])
            return True
        else:
            return False


    def execute_order(self):

        account = self.user.account
        account.processing_lock = True
        account.save(update_fields=['processing_lock'])

        if self.is_valid():
            coin_price = get_current_ETH_price()

            if self.type=='Buy':
                account.cash -= self.amount*coin_price['price']
                account.coin += self.amount
                account.timestamp_latest_activity = timezone.now()
            else:
                account.coin -= self.amount
                account.cash += self.amount*coin_price['price']
                account.timestamp_latest_activity = timezone.now()

            self.change_order_status('Success')
            account.processing_lock = False
            account.save()
            return True

        else:
            self.cancel_order()
            account.processing_lock = False
            account.save(update_fields=['processing_lock'])
            return False


#Order cannot be executed, make sure order amount does not ' \
#                      'exceed account balance or daily limit'


