from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render
from trade.forms import TradeForm, OrderHistoryForm
from user_login.forms import LoginForm
from django.shortcuts import render, redirect
from get_price import get_current_ETH_price
from trade.models import Order, Account


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def common_info(user):
    user_num_of_coins = user.account.coin
    user_cash = user.account.cash
    coin_price = get_current_ETH_price()['price']

    return {
        'coin': user_num_of_coins,
        'cash': user_cash,
        'parent_page': 'trade',
        'page': type,
        'rate': coin_price,
        'rate_str': "{0:.2f}".format(coin_price)}



def display_order_history(request):
    if not request.user.is_authenticated():
        empty_Form = LoginForm()
        return render(request, "user_login/login_or_signup.html", {'header': 'Login', 'form': empty_Form}, status=403)

    if request.method == "POST":
        form = OrderHistoryForm(request.POST)

        if form.is_valid():
            orders = Order.objects.get_past_orders_for_user(request.user,
                                                        status=form.cleaned_data['status_type'],
                                                        timeframe=form.cleaned_data['interval'])
        else:
            orders = None
    else:
        form = OrderHistoryForm()
        orders = Order.objects.get_past_orders_for_user(request.user,
                                                        status='All',
                                                        timeframe='WEEK')

    return render(request, 'user_panel.html', merge_dicts(
        common_info(request.user),
        {'username': request.user.username,
         'header': 'Past Orders',
         'orders': orders,
         'form': form,
         'parent_page': 'trade',
         'page': 'order_history'}))


def display_buy_sell_panel(request, type):

    if not request.user.is_authenticated():
        empty_Form = LoginForm()
        return render(request, "user_login/login_or_signup.html", {'header': 'Login', 'form': empty_Form}, status=403)

    if request.method == 'GET':
        form = TradeForm()
    elif request.method == 'POST':
        form = TradeForm(request.POST)

        if form.is_valid():
            if type == 'sell':
                order = Order.objects.place_order_for_user(user=request.user,
                                                           type='Sell',
                                                           amount=form.cleaned_data['num_of_coins'])
                success = order.execute_order()

            elif type == 'buy':
                order = Order.objects.place_order_for_user(user=request.user,
                                                           type='Buy',
                                                           amount=form.cleaned_data['num_of_coins'])
                success = order.execute_order()
            else:
                raise Http404

            if success:
                messages.info(request, 'Order has executed')
            else:
                messages.error(request, 'Order has failed to execute')

            if type == 'buy':
                return redirect(reverse('display_buy'))
            else:
                return redirect(reverse('display_sell'))

        else:
            # form is invalid
            pass
    else:
        raise Http404

    return render(request, 'user_panel.html', merge_dicts(
        common_info(request.user),
        {'username': request.user.username,
         'form': form,
         'parent_page': 'trade',
         'page': type}))
