from django.contrib.auth.models import User
from trade.models import Order
from django.test import TestCase

# Create your tests here.


# a user must have one and only one account
from trade.models import Account


class TestAccount(TestCase):


    def test_account_is_created_when_user_is_created(self):

        user = User.objects.create_user(username="foo")

        self.assertEqual(Account.objects.filter(user=user).count(), 1)
        self.assertEqual(Account.objects.filter(user=user).first().id, user.account.id)


class TestOrder(TestCase):

    def test_place_order(self):
        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)

        self.assertEqual(Order.objects.filter(user=user).count(),1)



    def test_execute_order(self):

        user = User.objects.create_user(username='foo')
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=10.00)
        order.execute_order()

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
        last_update_time = order.last_updated_at
        order.cancel_order()

        self.assertEqual(Order.objects.filter(user=user).first().order_status,'Success')
        self.assertEqual(Order.objects.filter(user=user).first().last_updated_at, last_update_time)


