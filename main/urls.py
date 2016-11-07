from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.main_page, name='main_page'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
     url(r'^usermenu/$', views.dashboard, name='usermenu'),
   ]