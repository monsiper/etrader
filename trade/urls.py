from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^buy/$', views.display_buy_sell_panel, {'type': 'buy'}, name='display_buy', ),
    url(r'^sell/$', views.display_buy_sell_panel, {'type': 'sell'}, name='display_sell'),
    url(r'^order_history/$', views.display_order_history, name='display_order_history'),

    ]