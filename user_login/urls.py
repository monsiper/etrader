from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^login/$', views.login_user, name='login'),
    url(r'^signup/$', views.signup_user, name='signup'),
    url(r'^logout/$', views.logout_user, name='logout'),
    ]