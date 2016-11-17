from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render
from trade.forms import TradeForm
from django.shortcuts import render, redirect
from get_price import get_current_ETH_price
from trade.models import Order, Account


def display_buy_sell_panel(request, type):
    from ipdb import set_trace
    # set_trace()
    user_num_of_coins = request.user.account.coin
    user_cash = request.user.account.cash
    coin_price = get_current_ETH_price()['price']

    form = TradeForm()

    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'GET':
        form = TradeForm()
    elif request.method == 'POST':
        form = TradeForm(request.POST)

        if form.is_valid():
            if type == 'sell':
                try:
                    order = Order.objects.place_order_for_user(user=request.user,
                                                               type='Sell',
                                                               amount=form.cleaned_data['num_of_coins'])
                    success = order.execute_order()
                except:
                    return HttpResponse("Unsuccesful because of exception")

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

    return render(request, 'user_panel.html', {'username': request.user.username,
                                               'form': form,
                                               'coin': user_num_of_coins,
                                               'cash': user_cash,
                                               'parent_page': 'trade',
                                               'page': type,
                                               'rate': coin_price,
                                               'rate_str': "{0:.2f}".format(coin_price)})
