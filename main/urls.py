from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.main_page, name='main_page'),
    # url(r'^panel/$', views.user_panel, name='panel'),
    url(r'^panel/profile/$', views.user_panel, {'type': 'profile'}, name='profile'),
    url(r'^panel/dashboard/$', views.user_panel, {'type': 'dashboard'}, name='dashboard'),
]
