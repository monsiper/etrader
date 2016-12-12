from django.contrib.auth.models import User
from trade.models import Order, Account, URL_ETH_PRICE
from django.test import TestCase
from ETH_price import get_price_from_web_api
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz,decimal
from trade.views import merge_dicts, common_info
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.

# a user must have one and only one account
class TestTradeViews(TestCase):

    def test_merge_dicts(self):
        dict_a = {'a':1, 'b':2, 'c':3}
        dict_b = {'d':5, 'e':8}
        self.assertEqual(len(merge_dicts(dict_a, dict_b)),5)
        dict_b = {}
        self.assertEqual(len(merge_dicts(dict_a, dict_b)), 3)

    def test_common_info(self):
        user = User.objects.create_user(username='foo')
        self.assertEqual(len(common_info(user)),4)

    def test_display_order_history(self):
        c = Client()
        # test case: anonymous user
        response = c.get(reverse('display_order_history'))
        self.assertEqual(response.status_code, 403)

        #test_case: authenticated user with GET
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        c.post(reverse('login'), {'email': 'john@adams.com', 'password': 'smith'})
        response = c.get(reverse('display_order_history'))
        self.assertEqual(response.status_code, 200)

        # test_case: authenticated user with POST
        response = c.post(reverse('display_order_history'), {'interval': 'WEEK', 'status_type': 'All'})
        self.assertEqual(response.status_code, 200)

    def test_display_buy_sell_panel(self):
        c = Client()
        # test case: anonymous user
        response = c.get(reverse('display_buy'))
        self.assertEqual(response.status_code, 403)
        response = c.get(reverse('display_sell'))
        self.assertEqual(response.status_code, 403)

        #test_case: authenticated user with GET
        User.objects.create_user(username='john@adams.com', email='john@adams.com', password='smith')
        c.post(reverse('login'), {'email': 'john@adams.com', 'password': 'smith'})
        response = c.get(reverse('display_buy'))
        self.assertEqual(response.status_code, 200)
        response = c.get(reverse('display_sell'))
        self.assertEqual(response.status_code, 200)

        # test_case: authenticated user with POST
        response = c.post(reverse('display_buy'),{})
        self.assertEqual(response.status_code, 200)
        response = c.post(reverse('display_buy'),{'num_of_coins': 400, 'amount': 200})
        self.assertEqual(response.status_code, 302)
        response = c.post(reverse('display_buy'),{'num_of_coins': 800, 'amount': 200})
        self.assertEqual(response.status_code, 302)
        response = c.post(reverse('display_sell'),{})
        self.assertEqual(response.status_code, 200)
        response = c.post(reverse('display_sell'),{'num_of_coins': 100, 'amount': 200})
        self.assertEqual(response.status_code, 302)
        response = c.post(reverse('display_sell'),{'num_of_coins': 500, 'amount': 200})
        self.assertEqual(response.status_code, 302)

        # response = c.post(reverse('display_sell'),{'num_of_coins': 500})
        # self.assertEqual(response.status_code, 302)
        # response = c.post(reverse('display_sell'),{'num_of_coins': 700})
        # self.assertEqual(response.status_code, 302)

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
        #test case: user account is active
        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)
        self.assertTrue(order)
        self.assertEqual(Order.objects.filter(user=user).count(),1)

        #test case: user account is inactive
        user.account.is_active = False
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=5.00)
        self.assertFalse(order)
        self.assertEqual(Order.objects.filter(user=user).count(),1)


    def test_execute_order(self):
        user = User.objects.create_user(username='foo')
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=100.00)
        self.assertEqual(order.execute_order(), True)
        self.assertEqual(Order.objects.filter(user=user).first().order_status, 'Success')
        #
        user = User.objects.get(username='foo')
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

        #test case: order coin amount > daily buy limit
        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=500.00)
        self.assertEqual(order.execute_order(),True)
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=500.00)
        self.assertEqual(order.execute_order(),True)
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=100.00)
        self.assertEqual(order.execute_order(), False)
        self.assertEqual(order.order_status, 'Fail')

        #test case: order sell amount > daily sell limit
        user.account.coin = decimal.Decimal(2000.00)
        user.account.save(update_fields=['coin'])
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=500.00)
        self.assertEqual(order.execute_order(),True)
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=500.00)
        self.assertEqual(order.execute_order(), True)
        order = Order.objects.place_order_for_user(user=user,type='Sell',amount=100.00)
        self.assertEqual(order.execute_order(), False)

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

        #test case: order cash amount > cash in the account
        user.account.cash = decimal.Decimal(1000.00)
        order.amount = decimal.Decimal(500.00)
        self.assertFalse(order.is_valid())

        #test case: order coin amount > coins in the account
        order.type = 'Sell'
        order.amount = decimal.Decimal(500.00)
        self.assertFalse(order.is_valid())


    def test_get_current_ETH_price(self):

        #test case: pulling price from an invalid site
        response = get_price_from_web_api('http://www.cnn.com/mehmetonsiper')
        self.assertEqual(response[0], 'Error')
        self.assertEqual(response[1], None)


        #test case: pulling price from the valid site
        response = get_price_from_web_api(URL_ETH_PRICE)
        self.assertEqual(response[0], 'Success')
        self.assertGreater(response[1], 0)


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

        #test case: get past orders with 'Pending' status
        list_of_orders = Order.objects.get_past_orders_for_user(user=user, status='Pending', timeframe='WEEK')
        self.assertFalse(list_of_orders)

        #
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


    def test_change_order_status(self):

        #test case: place order and try to change status to the previous status
        user = User.objects.create_user(username="foo")
        order = Order.objects.place_order_for_user(user=user,type='Buy',amount=10.00)
        self.assertFalse(order.change_order_status('Pending'))

        #test case: try to change status to one that is different from the previous status
        self.assertTrue(order.change_order_status('Success'))

        # test case: try to change status to something other than 'Pending','Success','Fail'
        self.assertFalse(order.change_order_status('Abc'))




