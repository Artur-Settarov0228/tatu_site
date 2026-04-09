from django.urls import path
from .views import DavomatListView, FanListView, JadvalListView

urlpatterns = [
    path('', DavomatListView.as_view(), name='davomat-list'),
    path('fans/', FanListView.as_view(), name='fan-list'),
    path('schedule/', JadvalListView.as_view(), name='jadval-list'),
]