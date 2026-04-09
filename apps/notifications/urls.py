from django.urls import path
from .views import XabarnomaListView

urlpatterns = [
    path('', XabarnomaListView.as_view(), name='xabarnoma-list'),
]