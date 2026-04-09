from django.urls import path
from .views import TalabaListView, TalabaDetailView, GuruhListView, KursListView, YonalishListView

urlpatterns = [
    path('', TalabaListView.as_view(), name='talaba-list'),
    path('<int:pk>/', TalabaDetailView.as_view(), name='talaba-detail'),
    path('groups/', GuruhListView.as_view(), name='guruh-list'),
    path('courses/', KursListView.as_view(), name='kurs-list'),
    path('directions/', YonalishListView.as_view(), name='yonalish-list'),
]