from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'getallissues$', views.getallissues, name='getallissues'),
    url(r'get_issues_in_last_24hrs/(?P<page_id>\w{1,10})$', views.get_issues_in_last_24hrs, name='getallissues'),
]