from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
import decimal
# Create your models here.
import logging

logger = logging.getLogger(__name__)

class AccountManager(models.Manager):

    def create_account_for_user(self, user):
        from ipdb import set_trace
        # set_trace()
        return self.create(user=user, cash=decimal.Decimal(10000.00), coin=decimal.Decimal(0.00))


@receiver(post_save, sender=User)
def create_account(instance, created, **kwargs):
    if created:
        Account.objects.create_account_for_user(instance)


# user.account_set.all() # rever
# user.accounts.all() #

# user.account
# account.user

class Account(models.Model):
    objects = AccountManager()
    cash = models.DecimalField(max_digits=8, decimal_places=3)
    coin = models.DecimalField(max_digits=8, decimal_places=3)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    buy_limit = models.DecimalField(max_digits=7, decimal_places=2, default=1000)
    sell_limit = models.DecimalField(max_digits=7, decimal_places=2, default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp_latest_activity = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    processing_lock = models.BooleanField(default=False)



class OrderManager(models.Manager):

    def place_order_for_user(self, user, type, amount):

        if user.account.is_active:
            return self.create(user=user,type=type, amount=decimal.Decimal(amount))
        else:
            return 'Cannot place order because account is disabled'


class Order(models.Model):

    ORDER_TYPE_CHOICES = (('Buy','BUY'), ('Sell','SELL'))

    ORDER_STATUS_CHOICES = (('Pending', 'Order is pending'),
                            ('Success', 'Order has executed'),
                            ('Fail','Order has failed'))

    objects = OrderManager()
    type = models.CharField(choices=ORDER_TYPE_CHOICES, blank=False, max_length=10)
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, default='Pending', max_length=10)
    placed_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
    # history = models.JSONField()

    def is_valid(self):

        account = self.user.account

        if self.type == 'Buy':
            return not (self.amount > account.buy_limit or self.amount*decimal.Decimal(11.98) > account.cash)
        else:
            return not (self.amount > account.sell_limit or self.amount > account.coin)


    def change_order_status(self, new_status):

        if new_status in ['Pending', 'Success', 'Fail'] and self.order_status != new_status:

            self.order_status = new_status
            self.last_updated_at = timezone.now()
            self.save(update_fields=['order_status','last_updated_at'])


    def cancel_order(self):

        if self.order_status == 'Pending':
            self.order_status = 'Fail'
            self.last_updated_at = timezone.now()
            self.save(update_fields=['order_status','last_updated_at'])

    def execute_order(self):

        if self.order_status == 'Pending':

            account = self.user.account
            account.processing_lock = True
            account.save(update_fields=['processing_lock'])

            if self.type=='Buy':
                account.cash -= self.amount*decimal.Decimal(11.98)
                account.coin += self.amount
                account.timestamp_latest_activity = timezone.now()

            else:
                account.coin -= self.amount
                account.cash += self.amount*decimal.Decimal(11.98)
                account.timestamp_latest_activity = timezone.now()

            account.processing_lock = False
            account.save()
            self.change_order_status('Success')

        else:

            return 'Cannot execute a finished order'




