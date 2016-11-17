from django.contrib.auth.models import User
from trade.models import Order, Account
from django.test import TestCase
from get_price import get_current_ETH_price

# Create your tests here.


# a user must have one and only one account


class TestAccount(TestCase):

    def test_create_account_for_user(self):
        user = User.objects.create_user(username='foo')
        self.assertEqual(Account.objects.filter(user=user).count(), 1)
        self.assertEqual(Account.objects.filter(user=user).first().id, user.account.id)
        self.assertIsNone(Account.objects.create_account_for_user(user))



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


