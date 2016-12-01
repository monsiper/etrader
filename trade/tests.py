from django.contrib.auth.models import User
from trade.models import Order, Account
from django.test import TestCase
from get_price import get_current_ETH_price
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz


# Create your tests here.


# a user must have one and only one account


class TestAccount(TestCase):

    def test_create_account_for_user(self):
        user = User.objects.create_user(username='foo')
        self.assertEqual(Account.objects.filter(user=user).count(), 1)
        self.assertEqual(Account.objects.filter(user=user).first().id, user.account.id)
        self.assertIsNone(Account.objects.create_account_for_user(user))

    def test_is_daily_limit_exceeded(self):
        user = User.objects.create_user(username='foo')
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=50.00)
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=250.00)
        self.assertFalse(user.account.is_daily_limit_exceeded(order))
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=700.00)
        self.assertFalse(user.account.is_daily_limit_exceeded(order))



class TestOrder(TestCase):


    def test_place_order(self):
        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)

        self.assertEqual(Order.objects.filter(user=user).count(),1)


    def test_execute_order(self):

        user = User.objects.create_user(username='foo')
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=10.00)
        self.assertEqual(order.execute_order(), True)
        self.assertEqual(Order.objects.filter(user=user).first().order_status, 'Success')
        self.assertLess(user.account.cash, 10000.00)


    def test_cancel_order(self):

        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)
        order.cancel_order()

        self.assertEqual(Order.objects.filter(user=user).first().order_status,'Fail')


    def test_cancel_order_after_execute(self):

        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)
        order.change_order_status('Success')
        self.assertEqual(order.cancel_order(),False)
        self.assertEqual(Order.objects.filter(user=user).first().order_status,'Success')


    def test_execute_order_greater_than_daily_limit(self):

        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=2000.00)
        self.assertEqual(order.execute_order(),False)
        self.assertEqual(order.order_status, 'Fail')

    def test_is_valid(self):

        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=200.00)
        order.change_order_status('Success')
        self.assertIsNone(order.is_valid())
        order.change_order_status('Fail')
        self.assertIsNone(order.is_valid())
        order.change_order_status('Pending')
        self.assertTrue(order.is_valid())

        order.amount = 2000.00
        self.assertFalse(order.is_valid())

        order.type = 'Sell'
        self.assertFalse(order.is_valid())

        order.amount = 500.00
        user.account.coin = 1000.00
        self.assertTrue(order.is_valid())


    def test_get_current_ETH_price(self):

        response = get_current_ETH_price()

        self.assertEqual(response['status'], 'Success')
        self.assertGreater(response['price'], 0)

    def test_get_past_orders_for_user(self):

        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=10.00)
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=5.00)
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=150.00)
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=32.00)
        order.execute_order()
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=150.00)
        order.execute_order()

        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Success', timeframe='WEEK')
        self.assertEqual(len(list_of_orders),4)
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Fail', timeframe='WEEK')
        self.assertEqual(len(list_of_orders),1)
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='All', timeframe='WEEK')
        self.assertEqual(len(list_of_orders),5)

        order.last_updated_at = datetime.now(pytz.utc) + relativedelta(days=-6)
        order.save(update_fields=['last_updated_at'])
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Fail', timeframe='WEEK')
        self.assertEqual(len(list_of_orders),1)
        order.last_updated_at = datetime.now(pytz.utc) + relativedelta(days=-7)
        order.save(update_fields=['last_updated_at'])
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Fail', timeframe='WEEK')
        self.assertEqual(len(list_of_orders),1)
        order.last_updated_at = datetime.now(pytz.utc) + relativedelta(days=-8)
        order.save(update_fields=['last_updated_at'])
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Fail', timeframe='WEEK')
        self.assertFalse(list_of_orders)





